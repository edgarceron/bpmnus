"""Manage common filter operation over models"""
from django.db.models import Q

class Filters():
    """Filters the corresponding models given a search string"""
    @staticmethod
    def picker_filter(model, value):
        """Filters the corresponding models for a picker"""
        search_type = 'contains'
        query = 'name__' + search_type
        return list(model.objects.filter(
            Q(active=True),
            Q(**{query: value})
        )[:10])

    @staticmethod
    def listing_filter(model, column, search, start, length, count=False):
        """Filters the corresponding models given a for a datatable"""
        search_type = 'contains'
        query = column + '__' + search_type
        if count:
            return model.objects.filter(
                Q(**{query: search})
            ).count()
        return model.objects.filter(
            Q(**{query: search})
        )[start:start + length]
