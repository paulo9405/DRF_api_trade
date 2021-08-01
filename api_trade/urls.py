from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ativos.api.viewsets import AtivoViewSet
from operacoes.api.viewsets import OperacaoViewSet
from operacoes.api.viewsets import UserViewSet

# aqui eu tenho as minhas urls que é o ponto entrada da minha aplicação, e toda url esta amarrado em uma viewSet,
# essa view vai receber a request...
router = routers.DefaultRouter()
router.register(r'ativos', AtivoViewSet)
router.register(r'operacoes', OperacaoViewSet, basename="operacoes")
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
