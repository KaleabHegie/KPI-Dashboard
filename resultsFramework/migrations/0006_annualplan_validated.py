# Generated by Django 4.2.13 on 2024-11-19 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultsFramework', '0005_quarterprogress_justification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='annualplan',
            name='validated',
            field=models.BooleanField(default=False),
        ),
    ]
