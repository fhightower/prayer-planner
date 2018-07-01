import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import generic

from .models import PrayerItem, JournalEntry, BiblePassage, DAYS_OF_WEEK


@register.filter
def get_item(dictionary, key):
    """This is a filter used in the IndexView to return the values at the given key of the given dictionary."""
    return dictionary.get(key)


def _is_correct_owner(prayer_item_id, current_user):
    """Check to see if the given prayer_item_id belongs to the current_user."""
    requested_item = PrayerItem.objects.get(pk=prayer_item_id)
    if requested_item.user.id == current_user.id:
        return True
    else:
        return False


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'prayers/index.html'

    def get(self, request):
        prayer_requests = dict()

        if not request.GET.get('s'):
            return redirect(reverse('prayers:index') + "?s=1#{}".format(DAYS_OF_WEEK[datetime.datetime.today().weekday()][1]))
        else:
            # for each day, collect the prayer requests for this day
            for day in DAYS_OF_WEEK:
                try:
                    prayer_requests[day[1]] = PrayerItem.objects.filter(day=day[0], user=request.user)
                except PrayerItem.DoesNotExist:
                    prayer_requests[day[1]] = []

            # get the most recent bible passage
            bible_passage = BiblePassage.objects.last()

            return render(request, self.template_name, {'prayer_requests': prayer_requests, 'days': [day[1] for day in DAYS_OF_WEEK], 'bible_passage': bible_passage})


class DetailRequestView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = PrayerItem

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        return _is_correct_owner(self.kwargs.get('pk'), self.request.user)


class MultiCreateRequestView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'prayers/prayeritem_multi_create.html'

    def post(self, request):
        request_titles = [title for title in dict(request.POST)['title'] if title != '']
        request_days = [day for day in dict(request.POST)['dayOfWeek'] if day != '']
        if len(request_titles) != len(request_days):
            messages.error(request, 'Found a different number of requests and days of the week... please make sure there is an equal number of things in the column on the left as the column on the right.')
            return HttpResponseRedirect(reverse('prayers:multi_create',))
        else:
            for index, request_title in enumerate(request_titles):
                new_prayer_item = PrayerItem(
                    title=request_title,
                    day=request_days[index],
                    user=request.user
                )
                new_prayer_item.save()
            return HttpResponseRedirect(reverse('prayers:index',))


class CreateRequestView(LoginRequiredMixin, generic.edit.CreateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    # TODO: I think this function can be removed
    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))

    def post(self, request, **kwargs):
        return self.save(request.POST.get('title'), request.POST.get('day'), request.POST.get('description'), request.user)

    def save(self, title, day, description, user):
        new_prayer_item = PrayerItem(title=title, day=day, description=description, user=user)
        new_prayer_item.save()
        return HttpResponseRedirect(reverse('prayers:details', args=(new_prayer_item.id,)))


class UpdateRequestView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    model = PrayerItem
    fields = ['title', 'day', 'description']

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        return _is_correct_owner(self.kwargs.get('pk'), self.request.user)

    def get_success_url(self):
        return reverse('prayers:details', args=(self.object.id,))


class UpdateJournalEntryView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.UpdateView):
    model = JournalEntry
    fields = ['text']

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        return _is_correct_owner(self.kwargs.get('prayer_item_pk'), self.request.user)

    def get_success_url(self, **kwargs):
        return reverse('prayers:details', args=(self.object.prayer_item.id,))


class CreateJournalEntryView(LoginRequiredMixin, UserPassesTestMixin, generic.edit.CreateView):
    model = JournalEntry
    fields = ['text']
    prayer_item_id = None

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        return _is_correct_owner(self.kwargs.get('pk'), self.request.user)

    def post(self, request, **kwargs):
        self.prayer_item_id = kwargs.get('pk')
        return self.save(request.POST.get('text'))

    def save(self, text):
        new_entry = JournalEntry(text=text, prayer_item=PrayerItem.objects.get(pk=self.prayer_item_id))
        new_entry.save()
        return HttpResponseRedirect(reverse('prayers:details', args=(self.prayer_item_id,)))


class DeletePrayerItemView(UserPassesTestMixin, generic.edit.DeleteView):
    model = PrayerItem
    success_url = reverse_lazy('prayers:index')

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        return _is_correct_owner(self.kwargs.get('pk'), self.request.user)


class DeleteJournalEntryView(UserPassesTestMixin, generic.edit.DeleteView):
    model = JournalEntry

    def get_login_url(self):
        return reverse('prayers:index',)

    def test_func(self):
        print("prayer_item_pk {}".format(self.kwargs['prayer_item_pk']))
        return _is_correct_owner(self.kwargs.get('prayer_item_pk'), self.request.user)

    def get_success_url(self, **kwargs):
        return reverse('prayers:details', args=(self.object.prayer_item.id,))


class CreatePassageView(LoginRequiredMixin, generic.edit.CreateView):
    model = BiblePassage
    fields = ['reference', 'text', 'note']

    def get_success_url(self):
        return reverse('prayers:index')
