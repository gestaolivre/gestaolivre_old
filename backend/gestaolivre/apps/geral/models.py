# -*- coding: utf-8 -*-
u"""Modelos gerais do Gestão Livre."""

import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.postgres.fields import JSONField
from django.db import models

from brazil_fields.fields import CNPJField

from gestaolivre.apps.utils.middleware import GlobalRequestMiddleware


def get_current_empresa(request=None):
    u"""Obtem a empresa selecionada através das informações do request."""
    if not request:
        request = GlobalRequestMiddleware.get_current_request()
    return request.user.domainuser.domains.first()


def get_current_empresa_pk(request=None):
    u"""Obtem a empresa selecionada através das informações do request."""
    return get_current_empresa(request).pk


class BaseModel(models.Model):
    u"""Modelo abstrato do Gestão Livre."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField(null=True)

    class Meta(object):
        abstract = True

    def __repr__(self):
        u"""Representação deste objeto."""
        return str(self)

    def __str__(self):
        u"""String que representa este objeto."""
        return '<{0}: {1}>'.format(self.__class__.__name__, self.id)


class Empresa(BaseModel):
    u"""Modelo abstrato especifico de uma empresa do Gestão Livre."""

    cnpj = CNPJField()
    razao_social = models.CharField(verbose_name='razão social',
                                    max_length=200)
    nome_fantasia = models.CharField(verbose_name='nome fantasia',
                                     max_length=100)

    class Meta(object):
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'


class UsuarioManager(BaseUserManager):
    u"""TODO: Documentar."""

    def create_user(self, email, nome, password=None):
        u"""Cria um usuário usando email e password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), nome=nome)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password):
        u"""Cria um super usuário usando email e password."""
        user = self.create_user(email, nome, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, BaseModel):
    u"""O usuário usado no Gestão Livre.

    No Gestão Livre não usamos o usuário padrão do Django para que possamos usar
    UUID como chaves primárias.
    """

    nome = models.CharField(max_length=200)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    empresa = models.ManyToManyField(Empresa)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def get_full_name(self):
        u"""TODO: Documentar."""
        return self.nome

    def get_short_name(self):
        u"""TODO: Documentar."""
        # The user is identified by their email address
        return self.email

    def __str__(self):
        u"""TODO: Documentar."""
        return self.email

    def has_perm(self, perm, obj=None):
        u"""TODO: Documentar."""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        u"""TODO: Documentar."""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        u"""TODO: Documentar."""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class PublicoModel(BaseModel):
    u"""Modelo compartilhado entre todas as empresas."""

    class Meta(object):
        abstract = True


class EmpresaModel(BaseModel):
    u"""Modelo privado de uma empresa."""

    empresa = models.ForeignKey(Empresa, default=get_current_empresa_pk)

    class Meta(object):
        abstract = True
