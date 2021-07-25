from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from operacoes.models import Operacao
from django.contrib.auth.models import User
from django.db.models import Sum


class OperacaoSerializer(ModelSerializer):
    class Meta:
        model = Operacao
        fields = [
            'id',
            'usuario_id',
            'ativo_id',
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
    saldo = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'saldo']

    def get_saldo(self, user):
        saldo = Operacao.objects.filter(
            usuario_id=user.id).aggregate(Sum('saldo'))
        return saldo['saldo__sum']
