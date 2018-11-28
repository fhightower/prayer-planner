from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from . import views

app_name="prayer_planner"
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path('prayers/', include('prayers.urls')),
    path(r'accounts/', include('accounts.urls')),
    path(r'admin/', admin.site.urls),
]
