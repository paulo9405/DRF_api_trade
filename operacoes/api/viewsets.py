from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from operacoes.models import Operacao, Configuracao
from operacoes.api.serializers import OperacaoSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.db.models import Sum


class OperacaoViewSet(viewsets.ModelViewSet):
    serializer_class = OperacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('ativo', 'tipo_operacao')
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Operacao.objects.filter(usuario_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        configuracao = Configuracao.objects.get(id=1)
        id_usuario = request.user.id
        ip = request.META.get("REMOTE_ADDR")
        ativo_id = request.data.get('ativo')
        quantidade = float(request.data.get('quantidade'))
        preco = float(request.data.get('preco'))
        tipo_operacao = request.data.get('tipo_operacao')
        operacao = Operacao.objects.create(
            usuario_id=id_usuario,
            ativo_id=ativo_id,
            quantidade=quantidade,
            preco=preco,
            tipo_operacao=tipo_operacao,
            ip=ip,
            custodia=configuracao.custodia,
            taxa_saque=configuracao.taxa_saque,
            administracao=configuracao.administracao
        )

        serialized_object = OperacaoSerializer(operacao)
        return Response(serialized_object.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.filter(id=self.request.user.id)
        return users

    @action(methods=["get"], detail=True)
    def saldo_por_ativo(self, request, pk=None):
        user = request.user
        ativo = request.query_params.get("ativo")
        saldo = Operacao.objects.filter(
            usuario_id=user.id, ativo__nome=ativo).aggregate(Sum('saldo'))
        return Response({ativo: saldo})
