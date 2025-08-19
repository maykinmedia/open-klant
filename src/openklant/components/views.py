from maykin_common.api_reference.views import (
    ComponentIndexView as BaseComponentIndexView,
)


class ComponentIndexView(BaseComponentIndexView):
    template_name = "index.html"
