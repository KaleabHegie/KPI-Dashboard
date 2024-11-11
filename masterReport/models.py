import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tinymce import models as tinymce_models
from resultsFramework.models import Quarter, Year

from userManagement.models import Account, ResponsibleMinistry, UserSector


# Options for report type
REPORT_TYPE_CHOICES = [
    ('3 months', '3 months'),
    ('6 months', '6 months'),
    ('9 months', '9 months'),
    ('Annual', 'Annual'),
]


    
class ReportGuideline(models.Model):
    section_title = models.CharField(max_length=550)
    section_word_limit = models.PositiveIntegerField()
    recorded_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.section_title


class ReportType(models.Model):
    type = models.CharField(max_length=1000)
    type_amh_name  = models.CharField(max_length=1000, blank=True)
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, related_name='report_quarters', null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null= True)

    report_guideline = models.ManyToManyField(ReportGuideline, blank=True)
    deadline = models.DateField(null=True)
    recorded_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = _("reporttype")
        verbose_name_plural = _("reporttypes")

        ordering = ['-created_at']

    def __str__(self):
        return self.type +" | "+ str(self.type_amh_name)

    def get_absolute_url(self):
        return reverse("reporttype_detail", kwargs={"pk": self.pk})

    def has_passed_deadline(self):
        today = datetime.date.today()     
        return self.deadline > today
    

class ReportSection(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    section_content = tinymce_models.HTMLField()
    word_count = models.IntegerField(default=0)
    recorded_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    report = models.ForeignKey("Report", on_delete=models.SET_NULL, null = True, blank = True)

 
    class Meta:
        verbose_name = _("report section")
        verbose_name_plural = _("report sections")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Report(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    alternative_name = models.CharField(max_length=150, null=True, blank=True)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    report_document = models.FileField(upload_to='masterReport/report_tables/', null=True, blank=True)
    recorded_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, related_name='ministry_report_quarters', null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null= True)
    
    responsible_ministry = models.ForeignKey("userManagement.ResponsibleMinistry", 
                                             on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")
        ordering = ['-created_at']
    
    def save(self,*args, **kwargs):
        self.name = self.responsible_ministry.responsible_ministry_eng +": " + str(self.report_type.year.year_amh)+"-"+self.report_type.type
        super(Report, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.quarter}-{self.year}-{self.responsible_ministry}'
    




    




class MasterReport(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    quarter = models.ForeignKey(
        Quarter, on_delete=models.SET_NULL, related_name='ministry_master_report_quarters', null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True)
    responsible_ministry = models.ForeignKey(ResponsibleMinistry, on_delete=models.SET_NULL, null=True)
    report_doc = models.FileField(upload_to='masterReport/document/', null=True, blank=True)
    report_type = models.ForeignKey(ReportType, on_delete=models.SET_NULL, null= True)
    seen = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _("Master_report")
        verbose_name_plural = _("Master_reports")
    
        unique_together = [
            ['quarter', 'year', 'responsible_ministry'],
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:  # Check if it's a new instance
            file_name = f"{self.quarter}-{self.year}-{self.responsible_ministry.responsible_ministry_eng}"
            self.name = f"{self.responsible_ministry.responsible_ministry_eng}: {self.year.year_amh}"

            # Retain the original extension
            original_extension = self.report_doc.name.split('.')[-1]
            self.report_doc.name = f"{file_name}.{original_extension}"

        super(MasterReport, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.quarter}-{self.year}-{self.responsible_ministry}'
