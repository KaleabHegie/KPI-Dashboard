from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import QuarterPlanTemp, QuarterProgress, NationalPlan, KpiAggregation, Quarter

@receiver(post_save, sender=QuarterPlanTemp)
def copy_quarter_plan_to_progress(sender, instance, created, **kwargs):

        # Assuming you have logic to determine the national plan
        national_plan = NationalPlan.objects.first()  # Replace with actual logic to determine the national plan
        
        # Assuming you have logic to determine the sub indicator

        
        # Retrieve the quarters
        quarters = list(Quarter.objects.all().order_by('id'))
        
        # Create a mapping of quarter numbers to targets
        quarters_targets = [
            (quarters[0], instance.quarter1_target),
            (quarters[1], instance.quarter2_target),
            (quarters[2], instance.quarter3_target),
            (quarters[3], instance.quarter4_target),
        ]

        # Create or update QuarterProgress entries for each quarter with a valid target
        for quarter, target in quarters_targets:
            if target is not None:
                quarter_progress, created = QuarterProgress.objects.update_or_create(
                    indicator=instance.indicator,
                    quarter=quarter,
                    year=instance.year,
                    defaults={'quarter_target': target}
                )

                if created:
                    print(f"Created QuarterProgress for {quarter} with target {target}")
                else:
                    print(f"Updated QuarterProgress for {quarter} with target {target}")
