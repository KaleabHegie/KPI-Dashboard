# Generated by Django 5.0.6 on 2024-06-01 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=200)),
                ('name_amh', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='KeyResultArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name_eng', models.CharField(max_length=350)),
                ('activity_name_amh', models.CharField(blank=True, max_length=350)),
                ('activity_weight', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('activity_is_shared', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NationalPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('np_name_eng', models.CharField(blank=True, max_length=150)),
                ('np_name_amh', models.CharField(blank=True, max_length=150)),
                ('description_eng', models.TextField()),
                ('description_amh', models.TextField()),
                ('starting_date', models.DateTimeField()),
                ('ending_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kpi_name_eng', models.CharField(max_length=100)),
                ('kpi_name_amh', models.CharField(blank=True, max_length=100)),
                ('kpi_weight', models.DecimalField(blank=True, decimal_places=3, max_digits=10)),
                ('kpi_measurement_units', models.CharField(max_length=50)),
                ('kpi_characteristics', models.CharField(choices=[('inc', 'Increasing'), ('dec', 'Decreasing'), ('const', 'Constant')], default='inc', max_length=10)),
                ('responsible_ministries', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userManagement.responsibleministry')),
                ('keyResultArea', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DashboardApp.keyresultarea')),
            ],
            options={
                'verbose_name': 'Key Performance Indicator',
            },
        ),
        migrations.CreateModel(
            name='DashboardSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_type', models.CharField(choices=[('month', 'Month'), ('quarter', 'Quarter'), ('year', 'Year')], max_length=200)),
                ('trend_type', models.CharField(choices=[('performance', 'Performance'), ('both', 'Both')], max_length=200)),
                ('dashboard_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.dashboardcategory')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.indicator')),
            ],
        ),
        migrations.CreateModel(
            name='StrategicGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_name_eng', models.CharField(blank=True, max_length=350)),
                ('goal_name_amh', models.CharField(blank=True, max_length=350, null=True)),
                ('goal_weight', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('goal_is_shared', models.BooleanField(default=False)),
                ('national_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DashboardApp.nationalplan')),
                ('responsible_ministries', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministry_goal', to='userManagement.responsibleministry')),
            ],
        ),
        migrations.AddField(
            model_name='keyresultarea',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kra_goal', to='DashboardApp.strategicgoal', verbose_name='Strategic Planning Goals'),
        ),
        migrations.AddIndex(
            model_name='keyresultarea',
            index=models.Index(fields=['goal'], name='DashboardAp_goal_id_9f7360_idx'),
        ),
    ]