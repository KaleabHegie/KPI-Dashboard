from django.core.management.base import BaseCommand
from resultsFramework.models import AnnualPlan2, AnnualPlan, NationalPlan, Year


class Command(BaseCommand):
    help = 'Copy records from AnnualPlan2 to AnnualPlan for specific years.'

    def handle(self, *args, **kwargs):
        np = NationalPlan.objects.first()
        if np:
            years_to_copy = ['2012', '2013', '2014',
                             '2015', '2016', '2017', '2018']

            for plan in AnnualPlan2.objects.all():
                for year in years_to_copy:
                    # Get the corresponding Year object for the current year
                    year_obj = Year.objects.get(year_amh=int(year))

                    # Try to get an existing AnnualPlan object for the year, indicator, and sub_indicator
                    annual_plan, created = AnnualPlan.objects.get_or_create(
                        national_plan=np,
                        indicator=plan.indicator,
                        sub_indicator=plan.sub_indicator,
                        year=year_obj,
                        defaults={
                            'annual_target': getattr(plan, f'plan_year_{year}', None),
                            'annual_performance': getattr(plan, f'performance_year_{year}', None),
                            'target_state': plan.target_state,
                        }
                    )

                    # If the AnnualPlan object was created or it already exists, save it
                    annual_plan.save()



            self.stdout.write(self.style.SUCCESS(
                'Successfully copied records from AnnualPlan2 to AnnualPlan.'))
        else:
            self.stdout.write(self.style.ERROR('Unable to copy records.'))
