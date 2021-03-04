"""Includes the data filters for pickers and datatables in the projects app"""
from django.db.models import Q
from projects.models import Projects

def project_picker_filter(value):
    """Given a value, filters projects for a select picker"""
    return list(Projects.objects.filter(
        Q(name__icontains=value)
    )[:10])

def project_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Projects.objects.filter(
            Q(name__icontains=search)
        ).count()

    return Projects.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]
