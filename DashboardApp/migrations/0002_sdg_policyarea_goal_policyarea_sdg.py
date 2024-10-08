# Generated by Django 4.2.13 on 2024-10-04 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='policyarea',
            name='goal',
            field=models.ManyToManyField(to='DashboardApp.strategicgoal'),
        ),
        migrations.AddField(
            model_name='policyarea',
            name='sdg',
            field=models.ManyToManyField(to='DashboardApp.sdg'),
        ),
    ]
