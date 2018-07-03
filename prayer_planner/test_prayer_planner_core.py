#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.test import TestCase


class ViewTests(TestCase):
    """View related tests."""

    def test_index_view(self):
        response = self.client.get('')
        assert response.status_code == 200
        assert 'Prayer Planner & Journal' in response.content.decode('utf-8')
