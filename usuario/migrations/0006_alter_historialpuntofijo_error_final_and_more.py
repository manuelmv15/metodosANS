# Generated by Django 5.2.2 on 2025-06-20 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_historialmetodo2_valoresmetodo2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialpuntofijo',
            name='error_final',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='historialpuntofijo',
            name='resultado_final',
            field=models.FloatField(null=True),
        ),
    ]
