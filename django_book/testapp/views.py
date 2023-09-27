#import json
from django.shortcuts import render
from django.core.paginator import Paginator

from datetime import datetime, timedelta, date

from rest_framework.response import Response
from rest_framework.views import APIView


from django_filters.rest_framework import DjangoFilterBackend

from django.db import models

from .serializers import (
    BooksListSerializer,
    BookDetailSerializer,
    DatesSerializer,
    FavoriteListSerializer,
    FavoriteMarkSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    BooksLastListSerializer,
    RubricsSerializer,
    RubricsSerializer2,
    RubricsSerializer4,
    RubricsCountSerializer,
    RubricsBooksSerializer,
    RubricsBooksSerializer1,
    BookDatesSerializer,
    SearchListSerializer
)

from rest_framework import generics, pagination

from .models import Books, Rubrics
from .utils import get_client_ip, BookFilter, get_date_ymd, nearest, get_date_ymd, StandardResultsSetPagination

'''
class BooksListView(APIView):
    """Вывод списка книг"""
    def get(self, request):
        # books = Books.objects.using('books').all()[:5]
        books = Books.objects.all().order_by("id").annotate(
            rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(request)))
        )[:5].annotate(
            avg_rating=models.Avg("rating__star")
        )
        serializer = BooksListSerializer(books, many=True)
        return Response(serializer.data)

'''


class BooksListView(generics.ListAPIView):
    """Вывод списка книг с возможностью фильтрации.
    GET /api/v1/first5/?rubrics=%D0%90%D1%83%D0%B4&title=&year_min=&year_max=
    """
    serializer_class = BooksListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        books = Books.objects.filter(id__lt=50).annotate(
            rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(self.request)))
        ).annotate(avg_rating=models.Avg("rating__star"))
        return books


class BooksLastListView(generics.ListAPIView):
    """Вывод простого списка последних загруженных книг"""
    serializer_class = BooksLastListSerializer

    def get_queryset(self):
        last_date = Books.objects.using('books').latest("date").date
        books = Books.objects.using('books').filter(date=last_date)
        return books
        #serializer = BooksLastListSerializer(books, many=True)
        #return Response(serializer.data)


class BookDetailView(generics.RetrieveAPIView):
    """Вывод полной информации по книге"""
    queryset = Books.objects.using('books').all()
    serializer_class = BookDetailSerializer

    """
    def get_queryset(self):
        qs = Books.objects.using('books').filter(id=self.kwargs.get('id'))
        #serializer = BookDetailListSerializer(book)
        return qs
    """
    


class FavoriteView(APIView):
    """Вывод списка избранного"""
    api_view = ['GET', 'PATCH']

    def get_object(self, pk):
        return Books.objects.using('books').get(id=pk)

    def patch(self, request):
        # book = self.get_object(request.query_params.get("pk"))
        book = self.get_object(request.data["pk"])
        favorite = FavoriteMarkSerializer(book, data=request.data, partial=True)
        if favorite.is_valid():
            favorite.save()
            return Response(status=201)
        return Response(status=400)

    def get(self, request):
        favorites = Books.objects.using('books').exclude(favorites__isnull=True)
        serializer = FavoriteListSerializer(favorites, many=True)
        return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к книге"""

    serializer_class = ReviewCreateSerializer
    """
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        print(review)
        if review.is_valid():
            review.save()
            return Response(status=201)
        return Response(status=400)
    """


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к книге"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
    """
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
    """


class BooksByRubricView(APIView):
    """Вывод книг по рубрикам без сериализаторов"""

    def get(self, request):
        last_date = Books.objects.using('books').latest("date").date
        books_last = Books.objects.using('books').filter(date=last_date)

        categories = []
        res_dict = {}

        for item in books_last:
            categories.append((item.rubrics_id, item.rubrics.rubric))

        categories = set(categories)

        for item in categories:
            temp_list = []
            temp_qs = books_last.filter(rubrics_id=item[0]).values()
            for i in temp_qs:
                temp_list.append({"author": i["author"], "title": i["title"]})

            # res_dict["rubric"+str(item)]=list(temp_list)
            res_dict[item[1]]=list(temp_list)

        # res = json.dumps(res_dict)
        #return JsonResponse(res_dict, safe=False, json_dumps_params={'ensure_ascii': False})
        return Response(res_dict)

class BooksByRubricView1(generics.ListAPIView):
    """Вывод ВСЕХ книг по рубрикам"""

    serializer_class = RubricsSerializer
    queryset = Rubrics.objects.all()
    """
        def get(self, request):
            last_date = Books.objects.using('books').latest("date").date
            books_last = Books.objects.using('books').filter(date=last_date)
            r = Rubrics.objects.all()
            serializer = RubricsSerializer(r, many=True)
            return Response(serializer.data)
    """

class BooksByRubricView2(generics.ListAPIView):
    """Вывод книг по рубрикам с сериализатором RubricsSerializer2 через FilteredListSerializer"""
    serializer_class = RubricsSerializer2
    queryset = Rubrics.objects.all()
    #def get_serializer_context(self):
    #    qs = super().get_queryset()
    #    date = self.request.GET['date']
    #    if date is None:
    #        return qs
    #    return qs.filter(date=date)
    #def get_queryset(self):
    #    r = Rubrics.objects.all()
    #    return r

class BooksByRubricView3(APIView):
    """Вывод книг по рубрикам с сериализатором RubricsSerializer2, но без generics"""
    def get(self, request):
        r = Rubrics.objects.all()
        serializer=RubricsSerializer2(r,many=True)
        return Response(serializer.data)


#worked
class BooksByRubricView4(generics.ListAPIView):
    """Вывод книг по рубрикам c возможностью запроса по дате загрузки date с сериализатором RubricsSerializer4 через FilteredListSerializer"""
    serializer_class = RubricsSerializer4
    queryset = Rubrics.objects.all()
    
    def get_serializer_context(self):
        return {'request': self.request}

class RubricsCountView(generics.ListAPIView):
    """Вывод книг по рубрикам c возможностью запроса по дате загрузки user_date с сериализатором RubricsSerializer4 через FilteredListSerializer"""
    serializer_class = RubricsCountSerializer
    queryset = Rubrics.objects.all()

#worked
class RubricsBooksView(generics.RetrieveAPIView):
    """Get books by rubric's id"""
    lookup_field = "id"
    #serializer_class = RubricsBooksSerializer
    serializer_class = RubricsBooksSerializer1
    #pagination_class = StandardResultsSetPagination
    #paginate_by = 10
    queryset = Rubrics.objects.all()


#worked
class DatesLast5View(APIView):
    """Вывод последних 5 дат загрузки до и после переданной даты или просто 5 последних"""
    #serializer = BookDatesSerializer
    #queryset = Books.objects.all().values('date').distinct()[:5]
    def get(self, request=None):
        request_date =self.request.query_params.get('date')
        date = request_date
        #First validation        
        if date:
            try:
                date1 = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                date = ''
        
        if date:
            dates_list = []
            dates_datelist=[]
            for item in Books.objects.all().values('date').distinct():
                dates_datelist.append(datetime.strptime(item['date'].split(' ')[0],'%Y-%m-%d'))
                dates_list.append(item['date'].split(' ')[0])
            #print(dates_list)
            try:
                date_index = dates_list.index(date)
            except ValueError:
                date = datetime.strftime(nearest(dates_datelist, datetime.strptime(date,'%Y-%m-%d')),'%Y-%m-%d')
                date_index = dates_list.index(date)
            try:
                date_from = dates_list[date_index+5]
            except IndexError:
                date_from = dates_list[len(dates_list)-1]
            try:
                if date_index-5 < 0:
                    date_to = dates_list[0]
                else:
                    date_to = dates_list[date_index-5]
            except IndexError:
                date_to = dates_list.first()
            #print('date_from:', date_from, 'date_to:', date_to)
            queryset = Books.objects.filter(date__gte=date_from, date__lte=date_to).values('date').distinct()
        else:
            queryset = Books.objects.all().values('date').distinct()[:5]
        res = DatesSerializer(queryset, many=True)
        return Response(res.data)
        

#worked
class SearchListView(generics.ListAPIView):
    """Вывод списка книг с возможностью фильтрации.
    GET /api/v1/search/?rubrics=&title=&year_min=&year_max=
    """
    serializer_class = SearchListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    pagination_class = StandardResultsSetPagination
    queryset = None    

    def get(self, request= None, *args, **kwargs):        
        title = self.request.query_params.get('title', None)
        if title:           
            queryset = Books.objects.all()
            #serializer_class = SearchListSerializer
            #filter_backends = (DjangoFilterBackend,)
            #filterset_class = BookFilter
            #queryset = None
            return super(SearchListView, self).get(request, *args, **kwargs)
        else:
            return(Response([]))        
    
    def get_queryset(self):
        queryset = self.kwargs.get(self.queryset)
        return queryset
    

def index(request):
    return render(request,"index.html")