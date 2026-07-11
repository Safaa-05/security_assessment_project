from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="security_dashboard"),
    path("scan/", views.scan, name="security_scan"),
    path("history/", views.history, name="security_history"),
    path("download/", views.download_report, name="download_report"),
]