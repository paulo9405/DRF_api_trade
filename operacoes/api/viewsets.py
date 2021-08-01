from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from operacoes.models import Operacao, Configuracao
from operacoes.api.serializers import OperacaoSerializer, UserSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.db.models import Sum


# quando a request chega aqui o django vai ver se ele é um post ou um get
# se ela chegar como um get, ela vai executar o get_queryset
# se ela chegar como post, vai ser executado o create, que tbm é um metodo padrao do django rest f
class OperacaoViewSet(viewsets.ModelViewSet):
    serializer_class = OperacaoSerializer
    # apos o get_queryset la em baixo no model operacao retornar algum objeto e
    # estiver com algum dado na mão, ele vai usar o operacaoSerializer para
    #transformar ele em json...

    filter_backends = [DjangoFilterBackend]
    filter_fields = ('ativo', 'tipo_operacao')
    http_method_names = ['get', 'post']

    def get_queryset(self):
        # essa funçao ela vai no banco usando o model e vai pegar o usuario da request, essa
        # request ja vem preenchida com o usuario, se eu estiver logado em outro browser com
        # outro usuario, o request id vai chegar diferente

        return Operacao.objects.filter(usuario_id=self.request.user.id)
        # pego todas as operaçoes desse usuario pelo method get_queryset que eu subscrevi o queryset, que é um metodo padrão do django
        # quando eu tenho o get_queryset aqui eu nao vou precisar se ter p queryset la em cima, ou é um ou é outro

    # nessa função eu sobscrevi o metodo create do django e pq quero ter controle do que acontece...
    def create(self, request, *args, **kwargs):
        configuracao = Configuracao.objects.all().first()
        # pego o objeto de configuração usando o first que vai ser o primeiro objeto que ele encontar, que são as taxas,

        id_usuario = request.user.id
        ip = request.META.get("REMOTE_ADDR")
        ativo_id = request.data.get('ativo')
        # toda request quando vem como POST, o form é convertido em forma de data(dados), os dados da request,
        # e desta varivel request.data eu pogo todas a informoções

        quantidade = float(request.data.get('quantidade'))
        preco = float(request.data.get('preco'))
        tipo_operacao = request.data.get('tipo_operacao')

        # dps q eu pego tudo que vem da request, eu uso o model para compor a operação, salvar..
        #dps eu uso o operacao serializer para serializer e retornar o json
        operacao = Operacao.objects.create( # retorno para linha 15
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

        #dps que crio a operação eu tenho que devolver ela para o usuario como json
        serialized_object = OperacaoSerializer(operacao)
        return Response(serialized_object.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer # aqui é parecido com operações

    def get_queryset(self):
        users = User.objects.filter(id=self.request.user.id)
        return users


    #aqui eu tnho um action personalizada (costm action), em vez d eeu ter só o create, post, put, delete e etc.. eu
    # criei minha propria action, dou o nome para ela de saldo_por_ativo, e defino qual o metodo que eu quero que
    # é p metodo 'get' que é só para consultar saldo, e o (detail=True) a função dele é quando estiver acessando o
    # usuario eu tenho que passar o id do usuario dps de usurs para poder ver o saldo só desse usuario
    # ex users/1/saldo_por_ativo/?ativo=bitcoin,
    # se eu colocar detail=False eu nao precisaria colocar o id, porem iria mostrar todos os saldos dos usuarios e isso nao pode
    @action(methods=["get"], detail=True)
    def saldo_por_ativo(self, request, pk=None):
        user = request.user # aqui recupero o usuario que quer ver o saldo
        ativo = request.query_params.get("ativo") #pego o ativo que passou no query_params

        # uso o model para pegar o dado que o usuario quer do banco, e faço o calculo dele usando a uma função 'aggregada'
        # que é o Sum, então eu busco todas as operações para esse usuario, onde o nome do ativo é seja o ativo que ele
        # passou no query_params, eu junto tudo somo e rotorno como saldo para ele, que nessse caso eu retono um dicionario
        # que ja é um json, o dicionario respeita o formato do json e ele ja éserializado por padrão por isso nao
        # precisei ter um serializer extra não..
        saldo = Operacao.objects.filter(
            usuario_id=user.id, ativo__nome=ativo).aggregate(Sum('saldo'))
        return Response({ativo: saldo})
