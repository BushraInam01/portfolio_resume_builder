from django.urls import path
from .views import (
    ResumeCustomizationView,
    ResumePreviewView,
    ResumePDFDownloadView,
)

app_name = "resumes"

urlpatterns = [
    path("customize/", ResumeCustomizationView.as_view(), name="customize"),
    path("preview/", ResumePreviewView.as_view(), name="preview"),
    path("download-pdf/", ResumePDFDownloadView.as_view(), name="download_pdf"),
]
