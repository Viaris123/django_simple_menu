from django.views.generic import TemplateView


class MenuExampleView(TemplateView):
    template_name = 'main/menu_example.html'
