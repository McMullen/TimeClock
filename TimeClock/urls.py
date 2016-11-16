"""
urls.py

@author Jason McMullen
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from TimeClock import views

admin.autodiscover()

urlpatterns = [
    url(r'', include('clock.urls')),
    url(r'^admin/', admin.site.urls),
]
