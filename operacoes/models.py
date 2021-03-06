from django.db import models
from django.contrib.auth.models import User
from ativos.models import Ativo


class Configuracao(models.Model):
    custodia = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    administracao = models.DecimalField(max_digits=6, decimal_places=2,
                                        default=0)
    taxa_saque = models.DecimalField(max_digits=6, decimal_places=2, default=0)


class Operacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    quantidade = models.DecimalField(max_digits=6, decimal_places=2)
    preco = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    custodia = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    administracao = models.DecimalField(max_digits=6, decimal_places=2,
                                        default=0)
    taxa_saque = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ip = models.GenericIPAddressField(null=True, blank=True)
    TIPO = (('Resgate', 'Resgate'), ('Aplicacao', 'Aplicacao'),)
    tipo_operacao = models.CharField(max_length=50, choices=TIPO)
    saldo = models.DecimalField(max_digits=6, decimal_places=2, default=0)


    # aqui eu subscrevi o metodo Save que o django tem, do models do django,
    # então eu criei o metodo seve, faço minhas proprias operaçoes de calculos...
    def save(self, *args, **kwargs):
        if self.tipo_operacao == 'Aplicacao':
            self.saldo = (float(self.quantidade) * float(self.preco)) -\
                         float(self.custodia) - float(self.administracao)

        elif self.tipo_operacao == 'Resgate':
            self.saldo = ((float(self.quantidade) * float(self.preco)) * -1) -\
                         float(self.taxa_saque)

        # retorno o metodo super que invoca o save da classe mae q o django tem, ele vai invocar o que esta acontecendo dentro do save, da parte do django, dps q eu
        # ja fiz tudo que queria fazer
        return super(Operacao, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.usuario) + ' - ' + str(self.ativo)
