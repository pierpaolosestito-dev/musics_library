"""musics_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.permissions import AllowAny

from musics.views import RegistrationView

API_TITLE = "Music Library"
API_DESCRIPTION = "SSD-SBM Organizations"
urlpatterns = [
    path('admin-rF17u22tkGM/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION, permission_classes=[AllowAny])),
    path('schema/', get_schema_view(title=API_TITLE, permission_classes=[AllowAny])),
    path('api/v1/musics/', include('musics.urls')),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    # path('api/v1/auth/registration/',include('dj_rest_auth.registration.urls')),
    path('api/v1/auth/registration/', RegistrationView.as_view())
]
