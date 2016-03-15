# -*- coding: utf-8 -*-
u"""Formulários do aplicativo geral."""

from django import forms

from .models import Empresa


class EmpresaForm(forms.ModelForm):
    u"""Formulário da Empresa."""

    class Meta:
        model = Empresa
        fields = ['nome_fantasia', 'razao_social', 'cnpj']
