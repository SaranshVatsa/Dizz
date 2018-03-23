"""datacheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,re_path, include
from django.conf.urls.static import static
from django.conf import settings
from dataapp_first import views
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$',views.root,name='root'),
    re_path('signin$',views.fileupload,name='signin'),
    re_path('charting$', views.charting,name='charting'),
    re_path('upload_csv$', views.upload_csv,name='upload_csv'),
    re_path('docaccess$', views.docaccess,name='docaccess')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
