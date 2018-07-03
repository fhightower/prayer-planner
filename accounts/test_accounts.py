#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.test import TestCase


class ViewTests(TestCase):
    """View related tests."""

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        assert response.status_code == 200
        assert 'Don\'t have an account yet? <a href="/accounts/register/">Register here</a>.' in response.content.decode('utf-8')
        assert 'Forgot your password? <a href="/accounts/password_reset/">Reset it here</a>.' in response.content.decode('utf-8')

    def test_register_view(self):
        response = self.client.get('/accounts/register/')
        assert response.status_code == 200
        assert response.content.decode('utf-8').count('<input type="') == 4
        assert 'Register for an Account!' in response.content.decode('utf-8')

    def test_password_reset_view(self):
        response = self.client.get('/accounts/password_reset/')
        assert response.status_code == 200
        assert '<input type="email"' in response.content.decode('utf-8')
        assert 'Reset your Password' in response.content.decode('utf-8')
