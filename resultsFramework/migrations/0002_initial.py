# Generated by Django 4.2.13 on 2024-11-11 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userManagement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resultsFramework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategicgoal',
            name='responsible_ministries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministry_goal', to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='sharedindicator',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_indicator', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='sharedindicator',
            name='responsible_ministry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='quarterprogress2',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_indicators_tempo', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='quarterprogress2',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_sub_indicator_tempo', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='quarterprogress2',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_indicators', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='quarter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarters', to='resultsFramework.quarter'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_sub_indicators', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='quarterprogress',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='quarterplantemp',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_indicators_temp', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='quarterplantemp',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='post',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_indicators', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='policyarea',
            name='sdg',
            field=models.ManyToManyField(blank=True, related_name='sdgs', to='resultsFramework.sdg'),
        ),
        migrations.AddField(
            model_name='planentrydate',
            name='yearOfEntry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='performanceentrydate',
            name='yearOfEntry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_indicators', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='months', to='resultsFramework.month'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='national_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.nationalplan'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='month_sub_indicators', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='monthprogress',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='month',
            name='quarter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.quarter'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.category'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='kpi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_kpi', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='kpiaggregation',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='keyresultarea',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kra_goal', to='resultsFramework.strategicgoal', verbose_name='Strategic Planning Goals'),
        ),
        migrations.AddField(
            model_name='indicatortempo',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kra_goal3', to='resultsFramework.strategicgoal', verbose_name='Strategic Planning Goals1'),
        ),
        migrations.AddField(
            model_name='indicatortempo',
            name='responsible_ministries',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministry_kpi3', to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='indicatormetadata',
            name='base_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='indicatormetadata',
            name='kpi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='goal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kra_goal_dashboard', to='resultsFramework.strategicgoal', verbose_name='goal dasboard'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='keyResultArea',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='indicators', to='resultsFramework.keyresultarea'),
        ),
        migrations.AddField(
            model_name='indicator',
            name='responsible_ministries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ministry_kpi', to='userManagement.responsibleministry'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='indicator',
            field=models.ManyToManyField(to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='month',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.month'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='quarter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.quarter'),
        ),
        migrations.AddField(
            model_name='dashboardsetting',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='annualquarter',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_quarter_indicators_tempo', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='annualplan2',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_indicators_tempo', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='annualplan2',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_sub_indicator_tempo', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_indicators', to='resultsFramework.indicator'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='national_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resultsFramework.nationalplan'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='sub_indicator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='annual_sub_indicators', to='resultsFramework.kpiaggregation'),
        ),
        migrations.AddField(
            model_name='annualplan',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resultsFramework.year'),
        ),
        migrations.AddField(
            model_name='agendagoals',
            name='sdg',
            field=models.ManyToManyField(blank=True, related_name='agenda_goals', to='resultsFramework.sdg'),
        ),
        migrations.AddField(
            model_name='quarterplanentrydate',
            name='quarter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_entry_performance', to='resultsFramework.quarter'),
        ),
        migrations.AddField(
            model_name='quarterperformanceentrydate',
            name='quarter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quarter_entry', to='resultsFramework.quarter'),
        ),
        migrations.AddIndex(
            model_name='keyresultarea',
            index=models.Index(fields=['goal'], name='resultsFram_goal_id_8fcc10_idx'),
        ),
        migrations.AddIndex(
            model_name='indicator',
            index=models.Index(fields=['kpi_name_eng', 'kpi_measurement_units'], name='resultsFram_kpi_nam_c81131_idx'),
        ),
    ]