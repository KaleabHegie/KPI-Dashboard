# Generated by Django 4.2.13 on 2024-06-02 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0003_remove_dashboardsetting_trend_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboardsetting',
            name='dashboard_category',
        ),
        migrations.AlterField(
            model_name='dashboardsetting',
            name='month',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.month'),
        ),
        migrations.AlterField(
            model_name='dashboardsetting',
            name='quarter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.quarter'),
        ),
    ]
