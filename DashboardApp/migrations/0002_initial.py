# Generated by Django 4.2.13 on 2024-06-03 21:41

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DashboardApp', '0001_initial'),
        ('userManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategicgoal',
            name='responsible_ministries',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministry_goal', to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_indicators', to='DashboardApp.indicator'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='national_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.nationalplan'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='quarter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarters', to='DashboardApp.quarter'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_sub_indicators', to='DashboardApp.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.year'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_indicators', to='DashboardApp.indicator'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='DashboardApp.month'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='national_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.nationalplan'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_sub_indicators', to='DashboardApp.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.year'),
        ),
        migrations.AddField(
            model_name='month',
            name='quarter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='DashboardApp.quarter'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DashboardApp.category'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='kpi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_kpi', to='DashboardApp.indicator'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='DashboardApp.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='keyresultarea',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kra_goal', to='DashboardApp.strategicgoal', verbose_name='Strategic Planning Goals'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='keyResultArea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicators', to='DashboardApp.keyresultarea'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='responsible_ministries',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='indicator',
            field=models.ManyToManyField(to='DashboardApp.indicator'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='month',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.month'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='quarter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.quarter'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.year'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_indicators', to='DashboardApp.indicator'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='national_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='DashboardApp.nationalplan'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_sub_indicators', to='DashboardApp.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DashboardApp.year'),
        ),
        migrations.AddIndex(
            model_name='keyresultarea',
            index=models.Index(fields=['goal'], name='DashboardAp_goal_id_9f7360_idx'),
        ),
    ]
