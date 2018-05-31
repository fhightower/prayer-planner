#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """This is a wrapper of django's built-in user object so that it can be easily extended."""
