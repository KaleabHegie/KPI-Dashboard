from django.core.management.base import BaseCommand
from resultsFramework.models import Indicator, StrategicGoal


class Command(BaseCommand):
    help = 'Update responsible ministry for StrategicGoals based on associated Indicators.'

    def handle(self, *args, **kwargs):
        # Get all the Indicators
        indicators = Indicator.objects.all()

        for indicator in indicators:
            # Check if keyResultArea is not None before trying to access goal
            key_result_area = indicator.keyResultArea
            if key_result_area and key_result_area.goal:
                goal = key_result_area.goal

                # Update the responsible_ministries for the StrategicGoal with the Indicator's responsible_ministries
                goal.responsible_ministries = indicator.responsible_ministries
                goal.save()
            else:
                # Optionally, log or handle the case where keyResultArea or goal is missing
                self.stdout.write(self.style.WARNING(
                    f"Indicator {indicator.id} has no associated keyResultArea or goal."))

        self.stdout.write(self.style.SUCCESS(
            'Successfully updated responsible ministry for StrategicGoals.'))
