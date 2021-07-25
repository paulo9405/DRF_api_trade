from rest_framework.serializers import ModelSerializer
from ativos.models import Ativo


class AtivoSerializer(ModelSerializer):
    class Meta:
        model = Ativo
        fields = ['id', 'nome', 'modalidade']
