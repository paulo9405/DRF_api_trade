# Generated by Django 3.2.5 on 2021-07-22 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0006_rename_tipo_operacao_operacao_tipo_operacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operacao',
            old_name='tipo_operacao',
            new_name='Tipo_operacao',
        ),
    ]