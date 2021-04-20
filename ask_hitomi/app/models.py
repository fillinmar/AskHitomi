from django.db import models


# Create your models here.
class Author (models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    autor = models.ForeignKey('Author', on_delete=models.CASCADE)





