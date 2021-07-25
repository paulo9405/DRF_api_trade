from django.test import TestCase
from rest_framework.test import APIClient
from .models import Ativo


class AtivosTestCase(TestCase):
    def test_adicionar_ativo_not_none(self):
        ativo_nome = 'meu ativo teste'
        modalidade = "Cripto"
        client = APIClient()
        client.post('/ativos/', {'nome': ativo_nome, "modalidade": modalidade}, format='json')
        ativo_db = Ativo.objects.get(nome=ativo_nome)
        self.assertIsNotNone(ativo_db)

    def test_adicionar_ativo_nome_esta_correto(self):
        ativo_nome = 'meu ativo teste'
        modalidade = "Cripto"
        client = APIClient()
        client.post('/ativos/', {'nome': ativo_nome, "modalidade": modalidade}, format='json')
        ativo_db = Ativo.objects.get(nome=ativo_nome)
        self.assertEqual(ativo_db.nome, ativo_nome)