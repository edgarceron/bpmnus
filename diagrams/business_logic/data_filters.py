"""Includes the data filters for pickers and datatables in the projects app"""
from datetime import timedelta, datetime
from django.db.models import Q
from diagrams.models import Diagrams

def project_picker_filter(value):
    """Given a value, filters projects for a select picker"""
    return list(Diagrams.objects.filter(
        Q(name__icontains=value)
    )[:10])

def project_listing_filter(filters, count=False):
    """Filters the corresponding models given a search string"""
    filtered = Diagrams.objects.all()
    for i in filters:
        field = i['id']
        if i['type'] == 'Text':
            param = field + '__icontains'
            filtered = filtered.filter(
                **{param: i['value']}
            )
        elif i['type'] == 'Range':
            min = i['value']
            max = i['value2']

            if min != "" and max != "":
                if i['options']['data_type'] == 'date':
                    min = datetime.strptime(min, '%Y-%m-%d')
                    max = datetime.strptime(max, '%Y-%m-%d') + timedelta(seconds=86399)
                param = field + '__range'
                filtered = filtered.filter(
                    **{param: (min, max)}
                )

            elif min != "":
                if i['options']['data_type'] == 'date':
                    min = datetime.strptime(min, '%Y-%m-%d')
                param = field + '__gte'
                filtered = filtered.filter(
                    **{param: min}
                )

            elif max != "":
                if i['options']['data_type'] == 'date':
                    max = datetime.strptime(max, '%Y-%m-%d') + timedelta(seconds=86399)
                param = field + '__lte'
                filtered = filtered.filter(
                    **{param: max}
                )

    if count:
        return filtered.count()
    return filtered
