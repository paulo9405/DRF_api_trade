# Generated by Django 3.2.5 on 2021-07-21 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0004_auto_20210721_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativo',
            name='modalidade',
            field=models.CharField(choices=[('Renda Fixa', 'Renda Fixa'), ('Renda variável', 'Renda variável'), ('Cripto', 'Cripto')], max_length=50),
        ),
    ]
