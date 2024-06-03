# Generated by Django 4.2.13 on 2024-06-03 20:34

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnualPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_target', models.FloatField(blank=True, null=True)),
                ('annual_performance', models.FloatField(blank=True, null=True)),
                ('annual_date', models.DateTimeField(auto_now_add=True)),
                ('target_state', models.CharField(choices=[('cum', 'Cumulative'), ('net', 'Net')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=200)),
                ('name_amh', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DashboardCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_eng', models.CharField(max_length=200)),
                ('name_amh', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DashboardSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('performance', models.BooleanField(blank=True, default=False, null=True)),
                ('target', models.BooleanField(blank=True, default=False, null=True)),
                ('rank', models.IntegerField(blank=True, null=True)),
                ('is_score_card', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'ordering': ['rank'],
            },
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
            ],
            options={
                'verbose_name': 'Key Performance Indicator',
            },
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
            name='KpiAggregation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_kpi_name_eng', models.CharField(max_length=400)),
                ('sub_kpi_name_amh', models.CharField(max_length=400)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_amh', models.CharField(max_length=100)),
                ('month_english', models.CharField(max_length=100)),
                ('month_ranked', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MonthProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_target', models.FloatField(blank=True)),
                ('month_performance', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
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
            name='Quarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter_eng', models.CharField(blank=True, max_length=100, null=True)),
                ('quarter_amharic', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuarterProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quarter_target', models.FloatField(blank=True)),
                ('quarter_performance', models.FloatField(blank=True, null=True)),
                ('quarter_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreCardRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=25, samples=None)),
                ('starting', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ending', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_eng', models.IntegerField()),
                ('year_amh', models.IntegerField()),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['year_amh'],
            },
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
            ],
        ),
    ]
