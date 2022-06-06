from django.db import models


# Create your models here.
class Headline (models.Model):

    title = models.TextField()
    lang = models.TextField()
    source = models.TextField()
    image = models.TextField()
    date = models.TextField()
    link = models.TextField()
    

    def __str__(self) -> str:
        return self.title