# Generated by Django 4.2.13 on 2024-10-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0008_alter_agendagoals_sdg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyarea',
            name='sdg',
            field=models.ManyToManyField(blank=True, related_name='sdgs', to='DashboardApp.sdg'),
        ),
    ]
