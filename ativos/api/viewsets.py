from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from ativos.models import Ativo
from ativos.api.serializers import AtivoSerializer

# Aqui eu pego o model e vai no banco, e pego todos os ativos e jogo no queryset,
# queryset é a lista de coisas que aparece na tela quando acessa ativos
class AtivoViewSet(viewsets.ModelViewSet):
    queryset = Ativo.objects.all() # essa funçao ela vai no banco usando o model e vai pega todos os ativos

    serializer_class = AtivoSerializer
    # quando o quereset acima ja esta preenchido com o dado do banco de dados, o django rest framework
    # por de tras dos panos ele vai fazer um favor para mim, ele vai pegar o queryset acima e
    # vai serializer ele usando o serializer que eu passei 'AtivoSerializer' e trasformar ele em json

    filter_backends = [DjangoFilterBackend] # aqui é a funçao para filtrar os ativos por 'nome e modalidade' citados abaixo
    filter_fields = ('nome', 'modalidade')

# quando eu acesso o endpoint 'localhost/8000/ativos' ele me retorna a lista de ativos cadastrados