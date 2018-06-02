import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse
from django.views import generic

from .models import PrayerItem, JournalEntry, DAYS_OF_WEEK


@register.filter
def get_item(dictionary, key):
    """This is a filter used in the IndexView to return the values at the given key of the given dictionary."""
    return dictionary.get(key)


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'prayers/index.html'

    def get(self, request):
        prayer_requests = dict()

        for day in DAYS_OF_WEEK:
            try:
                prayer_requests[day[1]] = PrayerItem.objects.filter(day=day[0])
            except PrayerItem.DoesNotExist:
                prayer_requests[day[1]] = []

        return render(request, self.template_name, {'prayer_requests': prayer_requests, 'days': [day[1] for day in DAYS_OF_WEEK], 'today': datetime.datetime.today().strftime('%A')})


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = PrayerItem


class CreateRequestView(LoginRequiredMixin, generic.edit.CreateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))


class CreateJournalEntryView(LoginRequiredMixin, generic.edit.CreateView):
    model = JournalEntry
    fields = ['text']
    pk = None

    def post(self, request, **kwargs):
        self.pk = kwargs.get('pk')
        return self.save(request.POST.get('text'))

    def save(self, text):
        new_entry = JournalEntry(text=text, prayer_item=PrayerItem.objects.get(pk=self.pk))
        new_entry.save()
        return HttpResponseRedirect(reverse('prayers:details', args=(self.pk,)))
