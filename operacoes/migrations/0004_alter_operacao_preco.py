# Generated by Django 3.2.5 on 2021-07-22 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operacoes', '0003_auto_20210721_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operacao',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=6),
        ),
    ]
