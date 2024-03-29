from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

import re
import uuid

from .models import PdfFile


@api_view(["POST"])
def convert(request):
    try:
        user_html = request.data["data"]
    except KeyError:
        raise ParseError("Missing data field")

    font_config = FontConfiguration()
    pdf = HTML(string=user_html).write_pdf(font_config=font_config)

    response = HttpResponse(content_type="application/pdf")
    response.write(pdf)
    return response


@api_view(["POST"])
@transaction.atomic
def convert_with_metadata(request):
    try:
        user_html = request.data["data"]
    except KeyError:
        raise ParseError("Missing data field")

    soup = BeautifulSoup(user_html, features="html5lib")
    for index, a in enumerate(soup.find_all("a")):
        if "name" in a.attrs:
            a.attrs["name"] += f"-{index}"

    font_config = FontConfiguration()
    pdf_file = HTML(string=str(soup)).render(font_config=font_config)
    pdf_saved = pdf_file.write_pdf()
    data = [page.anchors for page in pdf_file.pages]

    pdf_suf = SimpleUploadedFile(
        "{}.pdf".format(str(uuid.uuid4())), pdf_saved, content_type="application/pdf"
    )
    db_obj = PdfFile.objects.create(pdf=pdf_suf, anchors=data)

    return Response({"id": db_obj.pk})


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def metadata(request, document_id):
    try:
        pdf_file = PdfFile.objects.get(id=document_id)
    except PdfFile.DoesNotExist:
        raise NotFound("Invalid ID")

    response = []
    for page in pdf_file.anchors:
        new_page = {}
        for anchor in page:
            anchor_search = re.search("(.*)-[0-9]+", anchor)
            if anchor_search is None:
                continue
            anchor_base_name = anchor_search.group(1)
            anchor_coords = [page[anchor]]

            if anchor_base_name in new_page:
                new_page[anchor_base_name] += anchor_coords
            else:
                new_page[anchor_base_name] = anchor_coords

        response.append(new_page)

    return Response(response)


@api_view(["GET"])
def doc(request, document_id):
    try:
        db_obj = PdfFile.objects.get(id=document_id)
    except PdfFile.DoesNotExist:
        raise NotFound("Invalid ID")

    return FileResponse(db_obj.pdf)


@api_view(["GET"])
def health(request):
    return Response({})
