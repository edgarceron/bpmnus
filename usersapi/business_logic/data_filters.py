"""Includes the data filters for pickers and datatables in the users app"""
from django.db.models import Q
from django.contrib.auth.models import User

def user_picker_filter(value):
    """Given a value, filters users for a select picker"""
    return list(User.objects.filter(
        Q(first_name__icontains=value)
    )[:10])

def user_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return User.objects.filter(
            Q(first_name__icontains=search)
        ).count()

    return User.objects.filter(
        Q(first_name__icontains=search)
    )[start:start + length]
