#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )
