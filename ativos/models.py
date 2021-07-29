from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=50)
    TIPO = (
        ('Renda Fixa', 'Renda Fixa'),
        ('Renda variável', 'Renda variável'),
        ('Cripto', 'Cripto')
    )
    modalidade = models.CharField(max_length=50, choices=TIPO)

    class Meta:
        unique_together = ['nome', 'modalidade']

    def __str__(self):
        return self.nome







