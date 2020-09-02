from django.db import models

# Create your models here.
class Link(models.Model):
    URL_of_website = models.URLField(unique=False)
    Number_of_Lines = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.URL_of_website
