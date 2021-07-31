from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from operacoes.models import Operacao
from django.contrib.auth.models import User
from django.db.models import Sum


class OperacaoSerializer(ModelSerializer):
    ativo_nome = SerializerMethodField()
    modalidade = SerializerMethodField()
    nome_usuario = SerializerMethodField()
    class Meta:
        model = Operacao
        fields = [
            'id',
            'usuario',
            'nome_usuario',
            'ativo',
            'ativo_nome',
            'modalidade',
            'quantidade',
            'preco',
            'tipo_operacao',
            'data',
        ]

    def get_ativo_nome(self, obj):
        return '%s' % (obj.ativo)

    def get_modalidade(self, obj):
        return '%s' % (obj.ativo.modalidade)

    def get_nome_usuario(self, obj):
        return '%s' % (obj.usuario)


class UserSerializer(ModelSerializer):
    saldo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'saldo']

    def get_saldo(self, user):
        saldo = Operacao.objects.filter(
            usuario_id=user.id).aggregate(Sum('saldo'))
        return saldo['saldo__sum']
