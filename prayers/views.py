import datetime

from django.views import generic
from django.shortcuts import render
from django.urls import reverse
from django.template.defaulttags import register

from .models import PrayerItem, DAYS_OF_WEEK


@register.filter
def get_item(dictionary, key):
    """This is a filter used in the IndexView to return the values at the given key of the given dictionary."""
    return dictionary.get(key)


class IndexView(generic.TemplateView):
    template_name = 'prayers/index.html'

    def get(self, request):
        prayer_requests = dict()

        for day in DAYS_OF_WEEK:
            try:
                prayer_requests[day[1]] = PrayerItem.objects.filter(day=day[0])
            except PrayerItem.DoesNotExist:
                prayer_requests[day[1]] = []

        return render(request, self.template_name, {'prayer_requests': prayer_requests, 'days': [day[1] for day in DAYS_OF_WEEK], 'today': datetime.datetime.today().strftime('%A')})


class DetailView(generic.DetailView):
    model = PrayerItem


class CreateView(generic.edit.CreateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))
