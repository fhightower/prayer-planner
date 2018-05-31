from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'prayer_planner/index.html'


class AboutView(generic.TemplateView):
    template_name = 'prayer_planner/about.html'
