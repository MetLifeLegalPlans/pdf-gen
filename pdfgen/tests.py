from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from weasyprint import HTML

from .models import PdfFile

TEST_LINES = (
    '<style type="text/css">',
    ".doc_container p {",
    "    page-break-inside: avoid;",
    "}",
    "</style>",
    "<html>",
    "<head>",
    '    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">',
    '    <style type="text/css">',
    "        body {",
    "            margin: 0;",
    "            padding: 0;",
    "        }",
    "    </style>",
    "</head>",
    '<body class="doc-container">',
    "    <a name='test_anchor'>",
    "        This is a test anchor.",
    "    </a>",
    "    <a name='test_anchor'>",
    "        This is a second test anchor.",
    "    </a>",
    "    <p>",
    "        We, the witnesses named below, sign our names to this document, after having observed John Doe",
    "        affix his or her signature to this document.",
    "    </p>",
    "    <p>",
    "        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at interdum sem. Fusce laoreet ornare "
    "        purus, eget dictum est pretium at. Pellentesque id risus arcu. Pellentesque dolor mi, congue sit amet erat"
    "        in, finibus tempor quam. Aenean volutpat enim quis massa vehicula, a posuere sem imperdiet. Fusce tempor, "
    "        nisl a euismod lacinia, nulla orci pellentesque mauris, ut maximus nisi nisl a leo. Integer dapibus non "
    "        eros non eleifend. Suspendisse iaculis tortor non purus mollis, pellentesque fringilla diam maximus. "
    "        Suspendisse eleifend turpis in tellus tempus, nec accumsan turpis vestibulum. Curabitur bibendum "
    "        condimentum nulla in aliquam."
    "    </p>" * 5,  # this adds enough text to make the pdf 2 pages
    "    <a id='bad_anchor'>",
    "        We don't care about this anchor because it has no name"
    "    </a>"
    "</body>",
    "</html>",
)

EXPECTED_METADATA = [{"test_anchor": [[75.0, 75.0], [247.859375, 75.0]]}, {}]


def create_old_data(test_html):
    pdf_file = HTML(string=test_html).render()
    pdf_saved = pdf_file.write_pdf()
    data = [page.anchors for page in pdf_file.pages]

    pdf_suf = SimpleUploadedFile("temp.pdf", pdf_saved, content_type="application/pdf")
    db_obj = PdfFile.objects.create(pdf=pdf_suf, anchors=data)

    return db_obj.pk


class TestPdfgenViews(APITestCase):

    def test_convert(self):
        """make sure convert returns a valid pdf"""
        test_html = "\n".join(TEST_LINES)
        response = self.client.post(reverse("pdfgen:convert"), {"data": test_html})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.content, bytes)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_convert_with_metadata(self):
        # make sure we get an index back from convert-with-metadata
        test_html = "\n".join(TEST_LINES)
        response = self.client.post(
            reverse("pdfgen:convert-with-metadata"), {"data": test_html}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        document_id = response.json()["id"]

        # make sure metadata returns the correct anchor locations
        response = self.client.get(reverse("pdfgen:metadata", args=[document_id]))
        anchors = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(anchors, EXPECTED_METADATA)

        # make sure doc returns a valid pdf
        response = self.client.get(reverse("pdfgen:doc", args=[document_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response, FileResponse)

        # test for invalid id
        response = self.client.get(reverse("pdfgen:metadata", args=[document_id + 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(reverse("pdfgen:doc", args=[document_id + 1]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # make sure old data doesn't fail
        old_data_id = create_old_data(test_html)
        response = self.client.get(reverse("pdfgen:metadata", args=[old_data_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
