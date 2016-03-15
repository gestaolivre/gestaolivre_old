# -*- coding: utf-8 -*-
u"""Modelos gerais do Gestão Livre."""

from django.contrib.auth import get_user_model


User = get_user_model()


class EmailModelBackend(object):
    u"""This is a ModelBacked that allows authentication with an email address."""

    def authenticate(self, **credentials):
        u"""Authenticate user by email."""
        print("Ops: " + str(credentials))
        try:
            user = User.objects.get(email=credentials['email'])
            if user.check_password(credentials['password']):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        u"""Get user by its email."""
        try:
            return User.objects.get(email=username)
        except User.DoesNotExist:
            return None
