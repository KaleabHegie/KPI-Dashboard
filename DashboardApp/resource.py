from import_export import fields, resources

from userManagement.models import ResponsibleMinistry
from .models import StrategicGoal, KeyResultArea
from import_export.widgets import ForeignKeyWidget

class GoalResource(resources.ModelResource):
    author = fields.Field(
        column_name='responsible_ministries',
        attribute='responsible_ministries',
        widget=ForeignKeyWidget(ResponsibleMinistry, field='responsible_ministry_eng'))
    class Meta:
        model = StrategicGoal