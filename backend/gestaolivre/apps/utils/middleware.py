# -*- coding: utf-8 -*-
u"""Middleware pare obter o request atual em qualquer função."""

from threading import local

_locals = local()


class GlobalRequestMiddleware(object):
    u"""Middleware pare obter o request atual em qualquer função."""

    def process_request(self, request):
        u"""Processa o request atual.

        Está função salva o request na thread atual, tornando-o acessivel de maneira global.
        """
        _locals.request = request

    @staticmethod
    def get_current_request():
        u"""Obtém o request da thread atual."""
        return getattr(_locals, 'request', None)
