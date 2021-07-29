from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from ativos.models import Ativo
from ativos.api.serializers import AtivoSerializer

class AtivoViewSet(viewsets.ModelViewSet):
    queryset = Ativo.objects.all()
    serializer_class = AtivoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('nome', 'modalidade')
