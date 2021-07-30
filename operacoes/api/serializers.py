from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from operacoes.models import Operacao
from django.contrib.auth.models import User
from django.db.models import Sum
from ativos.api.serializers import AtivoSerializer


class OperacaoSerializer(ModelSerializer):
    ativo = AtivoSerializer()

    class Meta:
        model = Operacao
        fields = [
            'id',
            'usuario',
            'ativo',
            'quantidade',
            'preco',
            'tipo_operacao',
            'data',
        ]


class SaldoSerializer(ModelSerializer):
    class Meta:
        model = Operacao
        fields = ['id', 'ativo', 'saldo']


class UserSerializer(ModelSerializer):
    saldo = serializers.SerializerMethodField(read_only=True) # ler o saldo por usuario,


    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'saldo']

    def get_saldo(self, user):
        saldo = Operacao.objects.filter(
            usuario_id=user.id).aggregate(Sum('saldo'))
        return saldo['saldo__sum']
