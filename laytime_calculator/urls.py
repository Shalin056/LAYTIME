# C:\Users\shali\Documents\shalin\test-app\laytime_calculator\urls.py
"""
URL configuration for laytime_calculator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# C:\Users\shali\Documents\shalin\test-app\laytime_calculator\urls.py

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('LAYTIME_UAT_API/',include('api.urls')),
    path('LAYTIME_UAT_API/workflow/',include('workflow.urls')),
    # path('api/',include('masters.urls')),
    path('LAYTIME_UAT_API/laytime/',include('laytime_details.urls'))
]
