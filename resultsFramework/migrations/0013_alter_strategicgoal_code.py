# Generated by Django 4.2.13 on 2024-11-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultsFramework', '0012_alter_policyarea_code_alter_strategicgoal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategicgoal',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
