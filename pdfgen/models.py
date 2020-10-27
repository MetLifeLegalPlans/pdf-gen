from django.db import models


class PdfFile(models.Model):
    pdf = models.FileField()
    anchors = models.JSONField(null=True, blank=True)
