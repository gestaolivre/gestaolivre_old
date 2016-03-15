# -*- coding: utf-8 -*-
u"""Configurações de URL do Gestão Livre."""

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from gestaolivre.apps.geral.views import EmpresaViewSet


router = DefaultRouter(trailing_slash=False)
router.register('geral/empresas', EmpresaViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include(router.urls)),
    url(r'^api/token-auth/', obtain_jwt_token),
    url(r'^api/token-refresh/', refresh_jwt_token),
    url(r'^api/token-verify/', verify_jwt_token),
]
