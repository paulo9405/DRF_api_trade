# Generated by Django 3.2.5 on 2021-07-21 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0002_saldo'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacao',
            name='saldo',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.DeleteModel(
            name='Saldo',
        ),
    ]
