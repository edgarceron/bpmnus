from django.db import models

# Create your models here.

class Projects(models.Model):
    """Model to represent a project"""
    name = models.TextField()
    desc = models.TextField()
    creation_date = models.DateTimeField()