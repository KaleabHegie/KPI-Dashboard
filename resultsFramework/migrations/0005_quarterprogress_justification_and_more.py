# Generated by Django 4.2.13 on 2024-11-14 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resultsFramework', '0004_annualplan_justification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quarterprogress',
            name='justification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='validation_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
