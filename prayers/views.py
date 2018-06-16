import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.urls import reverse
from django.contrib import messages
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

        print("request args {}".format(request.GET))

        if not request.GET.get('set'):
            return redirect(reverse('prayers:index') + "?set=1#{}".format(DAYS_OF_WEEK[datetime.datetime.today().weekday()][1]))
        else:
            for day in DAYS_OF_WEEK:
                try:
                    prayer_requests[day[1]] = PrayerItem.objects.filter(day=day[0])
                except PrayerItem.DoesNotExist:
                    prayer_requests[day[1]] = []

            return render(request, self.template_name, {'prayer_requests': prayer_requests, 'days': [day[1] for day in DAYS_OF_WEEK], 'today': datetime.datetime.today().strftime('%A')})


class DetailRequestView(LoginRequiredMixin, generic.DetailView):
    model = PrayerItem


class MultiCreateRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'prayers/prayeritem_multi_create.html'

    def post(self, request):
        request_titles = [request for request in dict(request.POST)['title'] if request != '']
        request_days = [request for request in dict(request.POST)['dayOfWeek'] if request != '']
        print("request request_titles {}".format(request_titles))
        print("request_days {}".format(request_days))
        if len(request_titles) != len(request_days):
            messages.error(request, 'Found a different number of requests and days of the week... please make sure there is an equal number of things in the column on the left as the column on the right.')
            return HttpResponseRedirect(reverse('prayers:multi_create',))
        else:
            for index, request_title in enumerate(request_titles):
                new_prayer_item = PrayerItem(
                    title=request_title,
                    day=request_days[index]
                )
                new_prayer_item.save()
            return HttpResponseRedirect(reverse('prayers:index',))


class CreateRequestView(LoginRequiredMixin, generic.edit.CreateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))


class UpdateRequestView(LoginRequiredMixin, generic.edit.UpdateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))


class UpdateJournalEntryView(LoginRequiredMixin, generic.edit.UpdateView):
    model = JournalEntry
    fields = ['text']

    def get_success_url(self, **kwargs):
        return reverse('prayers:details', args=(self.object.prayer_item.id,))


class CreateJournalEntryView(LoginRequiredMixin, generic.edit.CreateView):
    model = JournalEntry
    fields = ['text']
    prayer_item_id = None

    def post(self, request, **kwargs):
        self.prayer_item_id = kwargs.get('pk')
        return self.save(request.POST.get('text'))

    def save(self, text):
        new_entry = JournalEntry(text=text, prayer_item=PrayerItem.objects.get(pk=self.prayer_item_id))
        new_entry.save()
        return HttpResponseRedirect(reverse('prayers:details', args=(self.prayer_item_id,)))


def delete_request(request, **kwargs):
    entry = PrayerItem.objects.get(pk=kwargs['pk'])
    entry.delete()
    return HttpResponseRedirect(reverse('prayers:index',))


def delete_journal(request, **kwargs):
    journal_entry = JournalEntry.objects.get(pk=kwargs['pk'])
    journal_entry.delete()
    return HttpResponseRedirect(reverse('prayers:details', args=(kwargs['prayer_item_pk'],)))
