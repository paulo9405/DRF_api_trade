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
    # defino o nome da varialvel, ela vai adicionar um informação chamada saldo aos fields abaixo, e essa informação é o
    # retono da função la em baixo
    # o ready_only = True é pq esse campo nao pode ser editado, é somente leitura

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'saldo']


    # A função do serializer é simplesmente transformar informações em json, entao esse função 'get_saldo' nao
    # deveria esta aqui nao pertençe a esse lugar, esta resolvendo o problema, mas ela deveria estar no model usuario
    # porem estou usando o model usuario do django e não tenho o controle de colocar isso la, eu teria que criar meu
    # proprio model usuario, ter uma chave estrangeira para o 'user' do django, e la eu colocaria  o get_saldo e aqui
    # eu iria chamar ele...

    # pq o test falava q nao precisava criar um usuario...
    def get_saldo(self, user):                          # o django buscar o get mais o nome dela
        saldo = Operacao.objects.filter(                # busca todas a operações daquele usuario
            usuario_id=user.id).aggregate(Sum('saldo')) # da um Sum no campo saldo, explica ele no models
        return saldo['saldo__sum']                      # e aqui retorno o valor da soma, que o Sum retornou como saldo...
