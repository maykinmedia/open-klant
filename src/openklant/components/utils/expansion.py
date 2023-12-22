# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2023 Dimpact
import logging
from typing import Dict, Iterator, List, Optional, Tuple, Type, Union

from django.db import models
from django.utils.module_loading import import_string

from django_loose_fk.virtual_models import ProxyMixin
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.serializers import BaseSerializer, Field, Serializer
from rest_framework_inclusions.core import InclusionLoader
from rest_framework_inclusions.renderer import (
    InclusionJSONRenderer,
    get_allowed_paths,
    should_skip_inclusions,
)

from rest_framework.serializers import (
    BaseSerializer,
    ListSerializer,
    HyperlinkedModelSerializer,
)


logger = logging.getLogger(__name__)

EXPAND_KEY = "_expand"


class InclusionNode:
    """
    very simple implementation of the tree to display inclusions
    """

    def __init__(
        self,
        id: str,
        value: dict,
        label: str,
        many: bool,
        parent: "InclusionNode" = None,
    ):
        self.id = id
        self.value = value
        self.label = label
        self.many = many
        self.parent = parent
        self._children = []

        if self.parent:
            self.parent.add_child(self)

    def __str__(self):
        return f"{self.label}: {self.id}"

    def add_child(self, node: "InclusionNode"):
        self._children.append(node)

    def display_children(self) -> dict:
        """
        return dict where children are grouped by their label
        """
        results = {}
        for child in self._children:
            child_result = child.display()
            if child.many:
                results.setdefault(child.label, []).append(child_result)
            else:
                results[child.label] = child_result
        return results

    def display(self) -> dict:
        data = self.value.copy()
        if self._children:
            data[EXPAND_KEY] = self.display_children()
        return data

    def has_child(self, id) -> bool:
        return any(child.id == id for child in self._children)


class InclusionTree:
    """
    strictly speaking it's not a tree but a collection of nodes
    It's a little helper class to display nested inclusions
    """

    _nodes = []

    def add_node(
        self, id: str, value: dict, label: str, many: bool, parent_id: str = None
    ) -> None:
        if not parent_id:
            node = InclusionNode(id, value, label, many)
            self._nodes.append(node)
            return

        parent_nodes = [
            n for n in self._nodes if n.id == parent_id and not n.has_child(id)
        ]
        for parent_node in parent_nodes:
            node = InclusionNode(id, value, label, many, parent=parent_node)
            self._nodes.append(node)

    def display_tree(self) -> dict:
        result = {}
        root_nodes = [n for n in self._nodes if n.parent is None]

        for node in root_nodes:
            result[node.id] = node.display_children()
        return result


class ExpandLoader(InclusionLoader):
    """
    ExpandLoader is hugely inspired by 'InclusionLoader' from 'djangorestframework-inclusions'

    Unlike InclusionLoader ExpandLoader keeps track of the parent object of the inclusion
    and the path to this inclusion.
    It helps to back track each inclusion to the root objects.
    Since this change affects most of the methods, some copy-pasting is involved here
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._seen_external: Dict[str, ProxyMixin] = {}

    def inclusions_dict(self, serializer: Serializer) -> dict:
        """
        The method is used by the renderer.

        :param serializer: serializer with 'instance'
        :return dictionary which maps parent urls and related inclusions

        The example of the inclusions with 'expand=zaaktype,status,status.statustype':
        {
          <zaak1.url>: {
            "zaaktype": {...},
            "status": {
               ...
               "_expand": {
                 "statustype": {...}
               }
            }
          }
        }
        """

        tree = InclusionTree()
        request = serializer.context["request"]

        # add parent nodes to the tree
        instances = (
            serializer.instance
            if isinstance(serializer.instance, list)
            else [serializer.instance]
        )
        for instance in instances:
            tree.add_node(
                id=instance.get_absolute_api_url(request=request),
                label="",
                value={},
                many=False,
            )

        entries = self._inclusions((), serializer, serializer.instance)

        for obj, inclusion_serializer, parent, path, many in entries:
            data = (
                obj._initial_data
                if isinstance(obj, ProxyMixin)
                else inclusion_serializer(instance=obj, context=serializer.context).data
            )
            tree.add_node(
                id=data["url"],
                value=data,
                label=path[-1],
                many=many,
                parent_id=parent.get_absolute_api_url(request=request),
            )

        result = tree.display_tree()

        return result

    def _instance_inclusions(
        self,
        path: Tuple[str, ...],
        serializer: Serializer,
        instance: models.Model,
        inclusion_serializers: Optional[dict] = None,
    ):
        """
        add parameter 'inclusion_serializers'
        """
        inclusion_serializers = inclusion_serializers or getattr(
            serializer, "inclusion_serializers", {}
        )
        for name, field in serializer.fields.items():
            for entry in self._field_inclusions(
                path, field, instance, name, inclusion_serializers
            ):
                yield entry

    def _field_inclusions(
        self,
        path: Tuple[str, ...],
        field: Field,
        instance: models.Model,
        name: str,
        inclusion_serializers: Dict[str, Union[str, Type[Serializer]]],
    ) -> Iterator[
        Tuple[models.Model, Type[Serializer], models.Model, Tuple[str, ...], bool]
    ]:
        """
        change return of this generator from (obj, serializer_class) to
        (obj, serializer_class, parent_obj, path, many)
        """
        # if this turns out to be None, we don't want to do a thing
        if instance is None:
            return

        new_path = path + (name,)
        inclusion_serializer = inclusion_serializers.get(".".join(new_path))

        if isinstance(field, BaseSerializer) and not inclusion_serializer:
            for entry in self._sub_serializer_inclusions(new_path, field, instance):
                yield entry

            return

        if inclusion_serializer is None:
            return

        if isinstance(inclusion_serializer, str):
            inclusion_serializer = import_string(inclusion_serializer)

        many = True if hasattr(field, "child_relation") else False

        for obj in self._some_related_field_inclusions(
            new_path, field, instance, inclusion_serializer
        ):
            yield obj, inclusion_serializer, instance, new_path, many
            # when we do inclusions in inclusions, we base path off our
            # parent object path, not the sub-field
            for entry in self._instance_inclusions(
                new_path,
                inclusion_serializer(instance=object),
                obj,
                inclusion_serializers,
            ):
                yield entry

    def _some_related_field_inclusions(
        self,
        path: Tuple[str, ...],
        field: Field,
        instance: models.Model,
        inclusion_serializer: Type[Serializer],
    ) -> Iterator[models.Model]:
        """
        add handler for ListSerializer fields
        """
        if self.allowed_paths is not None and path not in self.allowed_paths:
            return []
        if isinstance(field, ListSerializer):
            return self._many_related_manager_field_inclusions(path, field, instance)

        if isinstance(field, HyperlinkedModelSerializer):
            return self._object_related_field_inclusions(path, field, instance)

        return super()._some_related_field_inclusions(
            path, field, instance, inclusion_serializer
        )

    def _many_related_manager_field_inclusions(
        self,
        path: Tuple[str, ...],
        field: Field,
        instance: models.Model,
    ):
        for obj in field.get_attribute(instance).all():
            if self._has_been_seen(obj):
                continue
            yield obj

    def _object_related_field_inclusions(
        self,
        path: Tuple[str, ...],
        field: Field,
        instance: models.Model,
    ):
        obj = field.get_attribute(instance)
        if self._has_been_seen(obj):
            return
        yield obj


class ExpandJSONRenderer(InclusionJSONRenderer, CamelCaseJSONRenderer):
    """
    Ensure that the InclusionJSONRenderer produces camelCase and properly loads loose fk
    objects
    """

    loader_class = ExpandLoader

    def _render_inclusions(self, data, renderer_context):
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")
        # if we have an error, return data as-is
        if response is not None and response.status_code >= 400:
            return None

        if not data:
            return None

        render_data = data.copy()

        if render_data and "results" in render_data:
            serializer_data = render_data["results"]
        else:
            serializer_data = render_data

        serializer = getattr(serializer_data, "serializer", None)
        # if there is no serializer (like for a viewset action())
        # we just pass the data through as-is
        if serializer is None:
            return None

        # if it's a custom action, and the serializer has no inclusions,
        # return the normal response
        view = renderer_context.get("view")
        if view is not None and hasattr(view, "action"):
            if not view.action:
                logger.debug("Skipping inclusions for view that has no action")
                return None
            action = getattr(view, view.action)
            if should_skip_inclusions(action, serializer):
                logger.debug(
                    "Skipping inclusion machinery for custom action %r", action
                )
                return None

        request = renderer_context.get("request")

        inclusion_loader = self.loader_class(get_allowed_paths(request, view=view))
        inclusions = inclusion_loader.inclusions_dict(serializer)

        if isinstance(serializer_data, list):
            for record in serializer_data:
                if record["url"] in inclusions:
                    record[EXPAND_KEY] = inclusions[record["url"]]

        if isinstance(serializer_data, dict):
            if inclusions.get(serializer_data["url"]):
                serializer_data[EXPAND_KEY] = inclusions[serializer_data["url"]]

        return render_data


def get_expand_options_for_serializer(
    serializer_class: Type[Serializer],
) -> List[tuple]:
    choices = [
        (
            opt,
            opt,
        )
        for opt in serializer_class.inclusion_serializers
    ]
    return choices
