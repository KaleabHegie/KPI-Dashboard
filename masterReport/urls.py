from django.urls import path
from .views import create_report,list_master_reports,detail_report,grid_quarter_report,update_report,pdf_report,viewMasterReport,view_mopd_report_active,view_mopd_report
    
urlpatterns = [
        path('create_report/<int:pk>/', create_report, name='create_report'),
        # path('list_master_reports/', list_master_reports, name='list_master_reports'),
        path('list_master_reports/', grid_quarter_report, name='view_quarter_reports'),
        path('reports/<int:pk>/', detail_report, name='detail_report'),
        path('update_report/<int:pk>/', update_report, name='update_report'),
        path('download-report/<int:pk>', pdf_report, name="report_pdf"),
        path('viewMasterReport/', viewMasterReport, name='viewMasterReport'),
        path('view_mopd_report_active/', view_mopd_report_active, name='view_mopd_report_active'), 

        path('view_mopd_report/', view_mopd_report, name='view_mopd_report'), 
  
]            