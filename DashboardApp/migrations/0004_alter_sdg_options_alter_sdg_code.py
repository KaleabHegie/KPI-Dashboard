# Generated by Django 4.2.13 on 2024-10-05 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0003_alter_sdg_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sdg',
            options={'ordering': ['code']},
        ),
        migrations.AlterField(
            model_name='sdg',
            name='code',
            field=models.IntegerField(unique=True),
        ),
    ]