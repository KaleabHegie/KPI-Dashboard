from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('resultsFramework.urls'), name='resultsFramework_urls'),
    path('report/', include('masterReport.urls'), name='masterReport_urls'),
    path('accounts/', include('userManagement.urls'), name='userManagement_urls'),
    path('comment/', include('comment.urls')),
    path('api/', include('comment.api.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('chat/', include('interactions.urls', namespace='interactions')),
    # path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
