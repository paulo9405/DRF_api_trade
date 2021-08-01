from django.test import TestCase
from ativos.models import Ativo
from .models import Operacao
from django.contrib.auth.models import User
from .api.serializers import UserSerializer


# eu fiz um teste simples, testando contra a api de 'ativos' pq faço um post nela, mas eu nao consegui fazer em operações o mesmo
# teste igual eu fiz em ativo, por que na minha view eu pego o usuario da request... e quando eu estou rodando o teste
# este usuario esta vazio, e eu nao sei como resolver..
# mas eu sei que na documentação tem alguma coisa mas eu ainda não cheguei a estudar essa parte,
# por exemplo 'ativos' não pega nada, se eu for na urls de ativo, ele nao faz nada, nao pega usuario de resquest
# por isso que em ativo funcionou o teste... agora para operação não funcionou pq é um pouco mais complexo.
# mas nem por isso vou deixar de testar operação, vou fazer os testes de que as aplicações e resgates devem conter
# no minimo as informações  abaixo, e entao eu crio as operações que o teste pediu como 'minimo' e vou certificar que
# vai funcionar

class OperacoesTestCase(TestCase):
    def setUp(
            self):  # os teste tem esse metodo chamado setUp que ele roda antes de tudo para preparar tudo que vc precisa para rodar, no caso aqui eu preciso cadastrasr um 'ativo' que é o bitcoin.
        credentials = {
            'username': 'paulo',
            'password': 'paulo@12345'}
        self.user = User.objects.create_user(**credentials)
        self.bitcoin = Ativo.objects.create(nome='bitcoin',
                                            modalidade="Cripto")  # crio um ativo de teste 'bitcoin', passo o nome e a modalidade. as letras tem q ser igual.

    # test para verificar se esta vazio ou não
    def test_criar_operacao_in_not_none(self):
        data = {
            "ativo": 1,
            # esse ativo foi criando no SetUp na hora q criei o bitcoin, como se o django cadastrou o bitcoin e eu consegui cadastrar uma operação para o ativo que o django criou

            "quantidade": 20,
            "preco": 100,
            "tipo_operacao": "Aplicacao"
        }

        # pego as variaves dentro do objeto data,
        operacao = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        self.assertIsNotNone(operacao)  # verifica se tem operação no banco ou nao

    # no setUp eu crio o bitcoin, eu faço um tste onde alguem q criou o bitcoin, e faço uma operação com esse bitcoin
    # que foi criado por outra pessoa... se o sistema nao tiver permitindo isso ele vai falhar
    # resumnindo Test criar operações com ativos de outros usuarios
    def test_criar_operacao_ativos_outros_usuarios(self):
        data = {
            "ativo": 1,  # foi criado no setUp na hora que criou o bitcoin
            "quantidade": 20,
            "preco": 100,
            "tipo_operacao": "Aplicacao"
        }

        operacao = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        self.assertIsNotNone(operacao)

    # verificando a aplicação
    def test_saldo_operacao_aplicacao(self):
        data = {
            "ativo": 1,
            "quantidade": 20,
            "preco": 100,
            "tipo_operacao": "Aplicacao"
        }

        operacao_aplicacao = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        self.assertEqual(operacao_aplicacao.saldo, 2000)
        # ou seja eu comprando 20 bitcois a 100 cada meu saldo tem que ser igual a 2000, se retornar outro valor esta errado.

    # operação resgate
    # nesse teste eu verifico fazendo uma aplicação de 2000 e um resegate de 1000 se meu saldo vai ser igual a 1000.
    def test_saldo_operacao_resgate(self):
        data = {
            "ativo": 1,
            "quantidade": 20,
            "preco": 100,
            "tipo_operacao": "Aplicacao"
        }

        operacao_aplicacao = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        data = {
            "ativo": 1,
            "quantidade": 10,
            "preco": 100,
            "tipo_operacao": "Resgate"
        }

        operacao_resgate = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        #self.assertEqual(operacao_resgate.saldo, 1000)
        data = UserSerializer(self.user).data
        self.assertEqual(data["saldo"], 1000)

    # nesse teste faço uma aplicação e um resgate incluindo as taxas.

    # eu gostaria de ter feito mais testes para operações onde eu iria verificar que eu não conseguia  ver operações
    # de outros usuarios, porem tive uma dificuldade com o django que a api de operaçoes ler o usuario da request,
    # e quando eu estou rodando o teste eu não tenho request, entao isso me travou e eu não sei como resolver mas
    # eu ja estou estudado para resolver isso pq sei que o django tem que ter alguma funcionalidade para min poder
    # resolver isso...
    def test_saldo_do_usuario(self):
        data = {
            "ativo": 1,
            "quantidade": 20,
            "preco": 100,
            "tipo_operacao": "Aplicacao",
            "custodia": 10,
            "administracao": 10,

        }

        Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
            custodia=data["custodia"],
            administracao=data["administracao"],

        )

        data = {
            "ativo": 1,
            "quantidade": 10,
            "preco": 100,
            "tipo_operacao": "Resgate",
            "taxa_saque": 10,
        }

        Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
            taxa_saque=data["taxa_saque"],
        )

        data = UserSerializer(self.user).data
        self.assertEqual(data["saldo"], 970)
