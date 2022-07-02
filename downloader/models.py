from django.db import models
from django.urls import reverse
class Url(models.Model):
    link = models.CharField(max_length=10000)

    def __str__(self):
        return self.link

    def get_absolute_url(self):
        return reverse("download_page")