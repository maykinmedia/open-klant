from .expansion import ExpandJSONRenderer


class APIMixin:
    """
    Determine the absolute URL of a resource in the API.

    Model mixin that reverses the URL-path in the API based on the
    ``uuid``-field of a model instance.
    """

    def get_absolute_api_url(self, request=None, **kwargs) -> str:
        from rest_framework.reverse import reverse

        """
        Build the absolute URL of the object in the API.
        """
        # build the URL of the informatieobject
        resource_name = self._meta.model_name
        app_name = request.resolver_match.app_name

        reverse_kwargs = {"uuid": self.uuid}
        reverse_kwargs.update(**kwargs)

        url = reverse(
            f"{app_name}:{resource_name}-detail",
            kwargs=reverse_kwargs,
            request=request,
        )

        return url


class ExpandMixin:
    renderer_classes = (ExpandJSONRenderer,)
    expand_param = "expand"

    def include_allowed(self):
        return self.action in ["list"]

    def get_requested_inclusions(self, request):
        # Pull expand parameter from request body in case of _zoek operation
        if request.method == "POST":
            return ",".join(request.data.get(self.expand_param, []))
        return request.GET.get(self.expand_param)
