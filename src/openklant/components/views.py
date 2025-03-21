from django.views.generic import TemplateView

from openklant import __homepage__, __version__


class ComponentIndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "active_notification_components": ["klantinteracties"],
                "component": self.kwargs.get("component"),
                "repository": __homepage__,
                "github_ref": __version__,
            }
        )
        return context
