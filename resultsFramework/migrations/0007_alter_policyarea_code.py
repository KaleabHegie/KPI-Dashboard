# Generated by Django 4.2.13 on 2024-11-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultsFramework', '0006_policyarea_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyarea',
            name='code',
            field=models.CharField(blank=True, editable=False, max_length=10, null=True, unique=True),
        ),
    ]
