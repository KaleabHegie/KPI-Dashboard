# Generated by Django 4.2.13 on 2024-11-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultsFramework', '0010_alter_policyarea_code_alter_strategicgoal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategicgoal',
            name='code',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True, unique=True),
        ),
    ]