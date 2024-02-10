from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=200, unique=True)
    born_date = models.DateField()
    born_location = models.CharField(max_length=300)
    description = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='tag')
        ]

    def __str__(self):
        return f"{self.name}"


class Quote(models.Model):
    quote = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'quote'], name='author quote')
        ]
