import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Article(models.Model):
    """Article"""
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articleDetail", kwargs={'pk': self.pk})


class Tag(models.Model):
    """Tag for article"""
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag
