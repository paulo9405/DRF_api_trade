from django.test import TestCase
from rest_framework.test import APIClient
from .models import Ativo

#criando um teste que testa a criação de ativos, eu achamo a api para cadastrar ativos,
# eu cadastro um e verifico se ele nao dar None
# castro um e verifico se o nome esta correto...
class AtivosTestCase(TestCase):
    def test_adicionar_ativo_not_none(self):
        ativo_nome = 'meu ativo teste'
        modalidade = "Cripto"

        client = APIClient() # crio o clinete a partir da  APIclient()

        client.post('/ativos/', {'nome': ativo_nome, "modalidade": modalidade}, format='json')
        #mando um POST na url ativos, mando o nome do ativo e da modalidade em  formato json

        ativo_db = Ativo.objects.get(nome=ativo_nome)
        # depois que mando o POST, vou no banco de dados e busco um ativo com o nome que criei em 'meu ativo teste'

        self.assertIsNotNone(ativo_db)
        # assert é verifique.. verifique que não é null, então a variavel 'ativo_db' não pode estar vazia,
        # se ela voltar vaizia vai dar pal, e quer dizer que mes sistema nao esta funcionando

    # esse aqui é a mesma coisa porem vai verificar se o ativo e o nome é igual o que eu passei  nas linhas 8, 9
    def test_adicionar_ativo_nome_esta_correto(self):
        ativo_nome = 'meu ativo teste'
        modalidade = "Cripto"
        client = APIClient()
        client.post('/ativos/', {'nome': ativo_nome, "modalidade": modalidade}, format='json')
        ativo_db = Ativo.objects.get(nome=ativo_nome)

        self.assertEqual(ativo_db.nome, ativo_nome)
        #verifica se foi cadastrada com o nome que mandei 'meu ativo teste'