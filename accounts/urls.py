#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'accounts'
urlpatterns = [
    path(r'login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path(r'register/', views.RegistrationView.as_view(), name='register'),
    path(r'password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path(r'password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path(r'password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    # path(r'^password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    # path(r'^reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_change_done.html'), name='password_reset_complete'),
    path(r'me/', views.ProfileView.as_view(), name='profile'),
]
