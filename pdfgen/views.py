from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from weasyprint import HTML

from .models import PdfFile


@api_view(["POST"])
def convert(request):
    try:
        user_html = request.data["data"]
    except KeyError:
        raise ParseError("Missing data field")

    pdf = HTML(string=user_html).write_pdf()

    response = HttpResponse(content_type="application/pdf")
    response.write(pdf)
    return response


@api_view(["POST"])
def convert_with_metadata(request):
    try:
        user_html = request.data["data"]
    except KeyError:
        raise ParseError("Missing data field")

    pdf_file = HTML(string=user_html).render()
    pdf_saved = pdf_file.write_pdf()
    data = [page.anchors for page in pdf_file.pages]

    pdf_suf = SimpleUploadedFile("temp.pdf", pdf_saved, content_type="application/pdf")
    db_obj = PdfFile.objects.create(pdf=pdf_suf, anchors=data)

    return Response({"id": db_obj.pk})


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def metadata(request, index):
    try:
        pdf_file = PdfFile.objects.get(id=index)
    except PdfFile.DoesNotExist:
        raise NotFound("Invalid ID")

    return Response(pdf_file.anchors)


@api_view(["GET"])
def doc(request, index):
    try:
        db_obj = PdfFile.objects.get(id=index)
    except PdfFile.DoesNotExist:
        raise NotFound("Invalid ID")

    return FileResponse(db_obj.pdf)
