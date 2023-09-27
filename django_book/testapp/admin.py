from django.contrib import admin


# Register your models here.
from .models import Books, Reviews, Rubrics, RatingStar, Rating


class BooksAdmin(admin.ModelAdmin):
    ordering = ['pubdate']
    search_fields = ['title', 'author']


admin.site.register(Books, BooksAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Reviews, ReviewsAdmin)


class RubricsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rubrics, RubricsAdmin)


class RatingStarAdmin(admin.ModelAdmin):
    pass


admin.site.register(RatingStar, RatingStarAdmin)


class RatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rating, RatingAdmin)
