from django.db import models
from django.utils import timezone

from accounts.models import User


DAYS_OF_WEEK = (
    ('Mon', 'Monday'),
    ('Tues', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thurs', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
)


class PrayerItem(models.Model):
    title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=5, choices=DAYS_OF_WEEK)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class JournalEntry(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    prayer_item = models.ForeignKey(PrayerItem, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.date_created:
            self.date_created = timezone.now()
        # self.modified = timezone.now()
        return super(JournalEntry, self).save(*args, **kwargs)


class BiblePassage(models.Model):
    reference = models.CharField(max_length=50)
    text = models.TextField()
    note = models.TextField()
