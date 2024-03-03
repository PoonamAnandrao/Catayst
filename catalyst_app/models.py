from django.db import models


# Create your models here.

class UploadedCSVFile(models.Model):
    file = models.FileField(upload_to='uploads/', null=True)

    def __str__(self):
        return str(self.file)
