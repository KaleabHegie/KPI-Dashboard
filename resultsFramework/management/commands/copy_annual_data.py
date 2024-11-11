from django.core.management.base import BaseCommand
from resultsFramework.models import AnnualQuarter, AnnualPlan, QuarterProgress, Year, Quarter, NationalPlan
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Copy data from AnnualQuarter to AnnualPlan and QuarterProgress'

    def handle(self, *args, **kwargs):
        # Copy data from AnnualQuarter to AnnualPlan
        np = NationalPlan.objects.first()
        annual_quarters = AnnualQuarter.objects.all()

        for annual_quarter in annual_quarters:
            try:
                # Update or create AnnualPlan for 2015
                annual_plan_2015, _ = AnnualPlan.objects.get_or_create(
                    national_plan=np,
                    indicator=annual_quarter.indicator,
                    year=Year.objects.get(year_amh='2015'),
                )
                setattr( annual_plan_2015 , 'annual_performance', annual_quarter.performance_2015)
                setattr(annual_plan_2015, 'target_state', 'cum')
                annual_plan_2015.save()

                # Update or create AnnualPlan for 2016
                annual_plan_2016, _ = AnnualPlan.objects.get_or_create(
                    national_plan=np,
                    indicator=annual_quarter.indicator,
                    year=Year.objects.get(year_amh='2016'),
                )
                setattr(annual_plan_2016, 'annual_target', annual_quarter.target_2016)
                setattr(annual_plan_2016, 'target_state', 'cum')
                annual_plan_2016.save()

                # Update or create AnnualPlan for 2017
                annual_plan_2017, _ = AnnualPlan.objects.get_or_create(
                    national_plan=np,
                    indicator=annual_quarter.indicator,
                    year=Year.objects.get(year_amh='2017'),
                )
                setattr(annual_plan_2017, 'annual_target', annual_quarter.target_2017)
                setattr(annual_plan_2017, 'target_state', 'cum')
                annual_plan_2017.save()

                # Update or create AnnualPlan for 2018
                annual_plan_2018, _ = AnnualPlan.objects.get_or_create(
                    national_plan=np,
                    indicator=annual_quarter.indicator,
                    year=Year.objects.get(year_amh='2018'),
                )
                setattr(annual_plan_2018, 'annual_target', annual_quarter.target_2018)
                setattr(annual_plan_2018, 'target_state', 'cum')
                annual_plan_2018.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error processing KPI (indicator: {annual_quarter.indicator}) - {str(e)}"
                ))

        # Copy data from AnnualQuarter to QuarterProgress
        # Add your code here if needed

        self.stdout.write(self.style.SUCCESS('Data copied successfully'))
