# Generated by Django 3.2.5 on 2021-07-21 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0003_ativo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativo',
            name='aprovado',
        ),
        migrations.RemoveField(
            model_name='ativo',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
