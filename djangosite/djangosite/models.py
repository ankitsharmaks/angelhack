from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=30)

class User(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=200)
    group = models.ForeignKey(Group)

class Tag(models.Model):
    name = models.CharField(max_length=30)
    score = models.FloatField()
    group = models.ForeignKey(Group)
