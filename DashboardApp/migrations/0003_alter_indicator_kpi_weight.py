# Generated by Django 4.2.13 on 2024-06-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indicator',
            name='kpi_weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
