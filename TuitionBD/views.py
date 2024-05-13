from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mgs"] = "Well come to our website"
        return context
    

