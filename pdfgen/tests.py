from django.http import FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
    "</body>",
    "</html>",
)

EXPECTED_METADATA = [{"test_anchor": [[75.0, 75.0], [247.859375, 75.0]]}]


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
