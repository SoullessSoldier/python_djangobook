from django_filters import rest_framework as filters

from rest_framework.response import Response
from .models import Books
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib import parse
import math

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class BookFilter(filters.FilterSet):
    #rubrics = CharFilterInFilter(field_name='rubrics__rubric', lookup_expr='icontains')
    rubrics = filters.CharFilter(field_name='rubrics__rubric', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    year = filters.RangeFilter()

    class Meta:
        model = Books
        #fields = ('rubrics', 'year')
        fields = ('rubrics', 'title', 'year')

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_page(self, url, max_page, direction = 'next'):
        qs = parse.parse_qs(parse.urlparse(url).query)
        if direction == 'next':
            if 'page' in qs:
                return int(qs['page'][0])
            else:
                return max_page
        elif direction == 'previous':
            if 'page' in qs:
                return int(qs['page'][0])
            else:
                return 1


    def get_paginated_response(self, data):
        max_number_of_pages = math.ceil(self.page.paginator.count / self.page_size)
        #real_number_of_pages = math.floor(self.page.paginator.count / self.page_size) 
        current_page = self.page.number
        #print(dir(self))
        #full_path = self.request.get_full_path()
        full_path = self.request.build_absolute_uri(self.request.get_full_path())
        #items_on_page = self.page.paginator.count - (self.page_size * current_page)        
        #items_on_page_rest = self.page.paginator.count * current_page % (self.page_size * number_of_pages)        
        return Response({
            'id':'',
            'rubric': 'Результат поиска',            
            'books': {
                'full_path': full_path,                
                'next_url': self.get_next_link(),
                'next': self.get_next_link() is not None, 
                'next_page_number': self.get_page(str(self.get_next_link()), max_number_of_pages, 'next'),
                'previous_url': self.get_previous_link(),
                'previous': self.get_previous_link() is not None,
                'previous_page_number': self.get_page(str(self.get_previous_link()), max_number_of_pages, 'previous'),
                'count': self.page.paginator.count,
                'pages': max_number_of_pages,
                'current_page': current_page,
                #'items_on_page': items_on_page,
                'data': data
            }
        })

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def get_date_ymd(date_txt):
    return date_txt.split(' ')[0]