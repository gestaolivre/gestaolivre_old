# -*- coding: utf-8 -*-
u"""Serializadores do aplicativo geral."""

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Empresa


class EmpresaSerializer(serializers.HyperlinkedModelSerializer):
    u"""Serializador do modelo Empresa."""

    self = serializers.SerializerMethodField()
    cnpj = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = ('self', 'cnpj', 'razao_social')
        extra_kwargs = {
            'parent': {'lookup_field': 'cnpj'}
        }

    def get_self(self, obj):
        u"""Obtem um link para este objeto."""
        request = self.context['request']
        return reverse(self.Meta.model.__name__.lower() + '-detail', kwargs={'cnpj': obj.cnpj.format('r')},
                       request=request)

    def get_cnpj(self, obj):
        u"""Obtem um link para este objeto."""
        return obj.cnpj.format('r')
