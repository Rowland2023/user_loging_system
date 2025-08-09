# your_project_name/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 🔑 This line includes the default Django authentication URLs.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # This should include your app's URLs
    path('', include('main.urls')),
]