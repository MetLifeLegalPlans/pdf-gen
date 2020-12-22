from django.urls import path

from . import views

app_name = "pdfgen"

urlpatterns = [
    path("convert/", views.convert, name="convert"),
    path("convert-with-metadata/", views.convert_with_metadata, name="convert-with-metadata"),
    path("metadata/<int:document_id>/", views.metadata, name="metadata"),
    path("doc/<int:document_id>/", views.doc, name="doc"),
    path("health/", views.health, name="health"),
]
