from django.db import models
from projects.models import Projects
# Create your models here.

class Diagrams(models.Model):
    """Model to represent a diagram"""
    project = models.ForeignKey(Projects, on_delete=models.DO_NOTHING)
    name = models.TextField()
    desc = models.TextField()
    xml = models.TextField()
    propierties = models.TextField()
    creation_date = models.DateTimeField()
