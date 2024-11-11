# copy_indicator_tempo.py

from django.core.management.base import BaseCommand
from resultsFramework.models import IndicatorTempo, Indicator,KeyResultArea
from django.db.models import Q


class Command(BaseCommand):
    help = 'Copy IndicatorTempo instances to Indicator'

    def handle(self, *args, **kwargs):
        indicators_to_copy = IndicatorTempo.objects.all()

        for indicator_tempo in indicators_to_copy:
            # Check if an Indicator with similar kpi_name_eng exists in different responsible_ministries
            existing_indicator = Indicator.objects.filter(
                Q(kpi_name_eng=indicator_tempo.kpi_name_eng) &
                ~Q(responsible_ministries=indicator_tempo.goal.responsible_ministries)
            ).first()

            if existing_indicator:
                # Update existing Indicator only if kpi_name_eng matches and in different responsible_ministries
                if existing_indicator.kpi_name_eng == indicator_tempo.kpi_name_eng:
                    existing_indicator.kpi_weight = indicator_tempo.kpi_weight
                    # Add more update conditions for other fields as needed

                    # Save the updated Indicator
                    existing_indicator.save()
            else:
                # If the Indicator does not exist, create a new one
                Indicator.objects.create(
                    kpi_name_eng=indicator_tempo.kpi_name_eng,
                    kpi_name_amh=indicator_tempo.kpi_name_amh,
                    kpi_weight=indicator_tempo.kpi_weight,
                    kpi_measurement_units=indicator_tempo.kpi_measurement_units,
                    kpi_characteristics=indicator_tempo.kpi_characteristics,
                    responsible_ministries=indicator_tempo.goal.responsible_ministries,
                    goal=indicator_tempo.goal,
                    kpi_is_visable=True,
                    # Copy other similar fields as needed
                )

        self.stdout.write(self.style.SUCCESS('Indicators copied and updated successfully.'))