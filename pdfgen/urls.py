from django.urls import path

from . import views

app_name = "pdfgen"

urlpatterns = [
    path("convert/", views.convert, name="convert"),
    path("convert-with-metadata/", views.convert_with_metadata, name="convert-with-metadata"),
    path("metadata/<int:index>/", views.metadata, name="metadata"),
    path("doc/<int:index>/", views.doc, name="doc"),
]
