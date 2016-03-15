# -*- coding: utf-8 -*-
u"""Views do aplicativo geral."""

from rest_framework import permissions
from rest_framework import viewsets

from .models import Empresa
from .serializers import EmpresaSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    u"""API da empresa."""

    queryset = Empresa.objects.all()
    lookup_field = 'cnpj'
    lookup_value_regex = '[0-9]+'
    serializer_class = EmpresaSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        u"""Cria uma empresa."""
        serializer.save()

    def get_queryset(self):
        u"""Obtém todas as empresas."""
        return Empresa.objects.all()
