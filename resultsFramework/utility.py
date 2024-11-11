from datetime import datetime
from django.db import models

from .models import Quarter, Year
# Create your models here.

class PlanEntryDate(models.Model):
    name = models.CharField(max_length=300)
    yearOfEntry = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def check_entryDate(self):
        if self.yearOfEntry and self.startDate <= datetime.now().date() <= self.endDate:
            return True
        return False

    def save(self, *args, **kwargs):
        # Update 'active' field based on 'check_entryDate' before saving
        self.active = self.check_entryDate
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        # Call the parent class' __init__ method
        super().__init__(*args, **kwargs)
        # Update 'active' field based on 'check_entryDate' during initialization
        self.active = self.check_entryDate


class QuarterPlanEntryDate(PlanEntryDate):
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, null=True, related_name="quarter_entry_performance")


class AnnualPlanEntryDate(PlanEntryDate):
    pass



class PerformanceEntryDate(models.Model):
    name = models.CharField(max_length=300)
    yearOfEntry = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def check_entryDate(self):
        if self.yearOfEntry and self.startDate <= datetime.now().date() <= self.endDate:
            return True
        return False

    def save(self, *args, **kwargs):
        # Update 'active' field based on 'check_entryDate' before saving
        self.active = self.check_entryDate
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        # Call the parent class' __init__ method
        super().__init__(*args, **kwargs)
        # Update 'active' field based on 'check_entryDate' during initialization
        self.active = self.check_entryDate


class QuarterPerformanceEntryDate(PerformanceEntryDate):
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, null=True, related_name="quarter_entry")


class AnnualPerformanceEntryDate(PerformanceEntryDate):
    pass
