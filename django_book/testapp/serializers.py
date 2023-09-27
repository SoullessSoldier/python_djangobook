from django.core.paginator import Paginator
from rest_framework import fields, serializers

from .models import Books, Rubrics, Reviews, Rating

from datetime import datetime



class RubricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubrics
        fields = "__all__"

class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр записей, только те, у кого parent=None"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивный вывод потомков"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class BooksListSerializer(serializers.ModelSerializer):
    """Список книг"""
    rating_user = serializers.BooleanField()
    avg_rating = serializers.FloatField()
    rubric_name = serializers.ReadOnlyField(source='rubrics.rubric')

    class Meta:
        model = Books
        # fields = "__all__"
        fields = ("id", "title", "author", "year", "pubdate", "date", "category", "rubrics", "rubric_name", "rating_user", "avg_rating")

#worked
class SearchListSerializer(serializers.ModelSerializer):
    """Список книг для функции поиска"""    
    rubric_name = serializers.ReadOnlyField(source='rubrics.rubric')
    #books = serializers.SerializerMethodField('paginated_books')
    #full_path = serializers.SerializerMethodField()

    class Meta:
        model = Books
        # fields = "__all__"
        fields = ("id", "cover", "title", "author", "year", "pubdate", "date", "category", "rubrics", "rubric_name")
        #fields = ("books",)
    
    '''
    def paginated_books(self, obj):
        page_size = self.context['request'].query_params.get('size') or 10
        print(obj)
        paginator = Paginator(obj.objects.all(), page_size)
        p_range = paginator.page_range
        page_number = self.context['request'].query_params.get('page') or 1
        if int(page_number) in p_range: 
            p_count= paginator.count
            p_pages = paginator.num_pages
            #page_number = self.context['request'].query_params.get('page') or 1
            current_page = paginator.page(page_number)
            if current_page.number == p_pages:
                p_page_has_next = False
                p_page_next_number = p_pages
            else: 
                p_page_has_next = current_page.has_next()
                p_page_next_number = current_page.next_page_number()
            if int(page_number) > 1:
                p_page_previous_number = current_page.previous_page_number()
            else:
                p_page_previous_number = 1
            p_page_has_previous = current_page.has_previous()
            books = current_page
            serializer = BookSerializer(books, many=True)
            return {'count': p_count, 'pages': p_pages, 'current_page': current_page.number,
                'next': p_page_has_next, 'next_page_number': p_page_next_number,  
                'previous': p_page_has_previous, 'previous_page_number': p_page_previous_number,
                'data': serializer.data}
    '''

class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Reviews
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ("name", "text", "children")


class BookDetailSerializer(serializers.ModelSerializer):
    """Список книг"""
    rubrics = serializers.SlugRelatedField(slug_field='rubric', read_only=True)
    reviews = ReviewSerializer(many=True)
    # rubrics = serializers.SlugRelatedField(slug_field='rubric', read_only=True, many=True) если несколько значений
    class Meta:
        model = Books
        exclude = ()


class FavoriteMarkSerializer(serializers.ModelSerializer):
    """Обновление избранного"""
    class Meta:
        model = Books
        fields = ("id", "favorites")


class FavoriteListSerializer(serializers.ModelSerializer):
    """Обновление избранного"""
    class Meta:
        model = Books
        fields = ("title", "author", "favorites")


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователя"""
    class Meta:
        model = Rating
        fields = ("star", "book")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get("ip", None),
            book=validated_data.get("book", None),
            defaults={"star": validated_data.get("star")}
        )
        return rating


class BooksLastListSerializer(serializers.ModelSerializer):
    """Вывод последних загруженных книг"""
    rubrics = serializers.SlugRelatedField(slug_field='rubric', read_only=True)
    class Meta:
        model = Books
        fields = ("id", "title", "author", "year", "pubdate", "date", "category", "rubrics")

#worked
class BookSerializer(serializers.ModelSerializer):
    rubric_name = serializers.ReadOnlyField(source='rubrics.rubric')
    class Meta:
        model = Books
        fields = (
            "id",
            "title",
            "author",
            "date",
            "cover",
            "rubric_name")

class RubricsSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Rubrics
        fields = ("rubric", "books",)


class FilteredListSerializer(serializers.ListSerializer):
    """Serializer to filter Book table, look for latest date for every rubric"""

    def to_representation(self, data):
        #pass
        latest_data = data.latest("date").date
        #latest_data = self.context.get("date")
        data = data.filter(date=latest_data)
        return super(FilteredListSerializer, self).to_representation(data)


class BookSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Books
        list_serializer_class = FilteredListSerializer
        fields = (
            "title",
            "author",
            "date")


class RubricsSerializer2(serializers.ModelSerializer):
    books = BookSerializer2(many=True, read_only=True)
    class Meta:
        model = Rubrics
        fields = ("rubric", "books",)

"""
class RubricSerializer(serializers.ModelSerializer):
    #rubrics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #books = RecursiveSerializer(many=True)
    #print(books)
    rubrics = RubricSerializer(read_only=True)
    #books = BooksListSerializer(many=True)
    class Meta:
        model = Books
        fields  = ("title", "rubrics",)
        #fields = ['rubric', 'rubrics']
        #fields = ['books', 'rubrics']
"""
#worked
class FilteredListSerializer4(serializers.ListSerializer):
    """Serializer to filter Book table, look for user provided date for every rubric"""

    def to_representation(self, data):
        obj = self.context['request'].query_params.get("date")
        if obj is not None:
            date = self.context['request'].query_params["date"]
        else: 
            date = data.latest("date").date
        data = data.filter(date=date)
        return super(FilteredListSerializer4, self).to_representation(data)
        
#worked
class BookSerializer4(serializers.ModelSerializer):
    class Meta:
        model = Books
        list_serializer_class = FilteredListSerializer4
        fields = (
            "id",
            "title",
            "author",
            "date",
            "pubdate",
            "cover")


class BookDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("date",)
        
#worked
class RubricsSerializer4(serializers.ModelSerializer):
    books = BookSerializer4(many=True, read_only=True)
    full_path = serializers.SerializerMethodField()
    class Meta:
        model = Rubrics
        fields = ("rubric", "full_path", "books")

    def get_full_path(self, obj):
        return self.context['request'].build_absolute_uri(self.context['request'].get_full_path())

class RubricsCountSerializer(serializers.ModelSerializer):

    books = serializers.SerializerMethodField()

    class Meta:
        model = Rubrics
        fields = ('rubric', 'books', 'id')

    def get_books(self, obj):
        books = Books.objects.filter(rubrics__in=[obj]).count()
        return books

class RubricsBooksSerializer(serializers.ModelSerializer):
    """Get books by rubric's id"""
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Rubrics
        fields =  ('id','rubric', 'books',)


class RubricsBooksSerializer1(serializers.ModelSerializer):
    books = serializers.SerializerMethodField('paginated_books')
    id = serializers.CharField()
    class Meta:
        model = Rubrics
        fields =  ('id','rubric', 'books',)
    def paginated_books(self, obj):
        full_path = self.context['request'].build_absolute_uri(self.context['request'].get_full_path())
        page_size = self.context['request'].query_params.get('size') or 10
        paginator = Paginator(obj.books.all(), page_size)
        p_range = paginator.page_range
        page_number = self.context['request'].query_params.get('page') or 1
        if int(page_number) in p_range: 
            p_count= paginator.count
            p_pages = paginator.num_pages
            #page_number = self.context['request'].query_params.get('page') or 1
            current_page = paginator.page(page_number)
            if current_page.number == p_pages:
                p_page_has_next = False
                p_page_next_number = p_pages
            else: 
                p_page_has_next = current_page.has_next()
                p_page_next_number = current_page.next_page_number()
            if int(page_number) > 1:
                p_page_previous_number = current_page.previous_page_number()
            else:
                p_page_previous_number = 1
            p_page_has_previous = current_page.has_previous()
            books = current_page
            serializer = BookSerializer(books, many=True)
            return {'full_path': full_path, 'count': p_count, 'pages': p_pages, 'current_page': current_page.number,
                'next': p_page_has_next, 'next_page_number': p_page_next_number,  
                'previous': p_page_has_previous, 'previous_page_number': p_page_previous_number,
                'data': serializer.data}


class DatesSerializer(serializers.ModelSerializer):
    #current_date = serializers.SerializerMethodField()
    class Meta:
        model = Books
        fields =  ('date',)
    def get_current_date(self, obj):        
        current_date = self.context['request_date'] or ''
        if current_date:
            try:
                date1 = datetime.strptime(current_date, '%Y-%m-%d')
            except ValueError:
                current_date = 'Invalid date'

        return current_date 