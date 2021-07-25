from django.db import models


class Ativo(models.Model):
    nome = models.CharField(max_length=50)
    TIPO = (
        ('Renda Fixa', 'Renda Fixa'),
        ('Renda variável', 'Renda variável'),
        ('Cripto', 'Cripto')
    )
    modalidade = models.CharField(max_length=50, choices=TIPO)


    def __str__(self):
        return self.nome







