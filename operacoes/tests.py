from django.test import TestCase
from ativos.models import Ativo
from .models import Operacao
from django.contrib.auth.models import User
from .api.serializers import UserSerializer


class OperacoesTestCase(TestCase):
    user = None
    bitcoin = None

    def setUp(self):
        credentials = {
            'username': 'paulo',
            'password': 'paulo@12345'}
        self.user = User.objects.create_user(**credentials)
        self.bitcoin = Ativo.objects.create(nome='bitcoin', modalidade="Cripto")

    def test_criar_operacao_in_not_none(self):
        data = {
            "ativo": 1,
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

    def test_criar_operacao_ativos_outros_usuarios(self):
        data = {
            "ativo": 1,
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
            "tipo_operacao": "Aplicacao"
        }

        operacao_resgate = Operacao.objects.create(
            usuario_id=self.user.id,
            ativo_id=data["ativo"],
            quantidade=data["quantidade"],
            preco=data["preco"],
            tipo_operacao=data["tipo_operacao"],
        )

        self.assertEqual(operacao_resgate.saldo, 1000)

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
