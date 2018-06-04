#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

app_name = 'prayers'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('request/create/', views.CreateRequestView.as_view(), name='create_request'),
    path('request/<int:pk>', views.DetailView.as_view(), name='details'),
    path('request/<int:pk>/update', views.UpdateRequestView.as_view(), name='update_request'),
    path('request/<int:prayer_item_pk>/journal/<int:pk>/edit', views.UpdateJournalEntryView.as_view(), name='update_journal'),
    path('request/<int:pk>/journal/create', views.CreateJournalEntryView.as_view(), name='create_journal'),
]
