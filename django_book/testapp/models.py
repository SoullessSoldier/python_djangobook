# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Books(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=555, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, unique=True, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    creator = models.CharField(max_length=255, blank=True, null=True)
    pubdate = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    format = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    quality = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    downloaded = models.BooleanField(blank=True, null=True)
    file = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    rating_plain = models.IntegerField(blank=True, null=True)
    turbocontentraw = models.CharField(max_length=255, db_column='turboContentRaw', blank=True, null=True)  # Field name made lowercase.
    rubrics = models.ForeignKey('Rubrics', on_delete=models.DO_NOTHING, related_name='books', blank=True, null=True)
    favorites = models.BooleanField(blank=True, null=True)
    source_site = models.TextField(blank=True, null=True)
    pages = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.author} - {self.title}"

    def __repr__(self):
        return f"{self.author} - {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        #managed = False
        db_table = 'books'
        ordering = ['-date']
        app_label = 'testapp'


class Rubrics(models.Model):
    id = models.AutoField(primary_key=True)
    rubric = models.CharField(max_length=255, blank=True, null=True)
    file = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.rubric}"

    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"
        #managed = False
        db_table = 'rubrics'
        app_label = 'testapp'
        ordering = ['id']


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=255)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL,
    blank=True, null=True, related_name="children")
    book = models.ForeignKey(Books, verbose_name="Книга", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.book}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = 'reviews'
        app_label = 'testapp'

class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]
        db_table = 'ratingstar'
        app_label = 'testapp'


class Rating(models.Model):
    ip = models.CharField(verbose_name="IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name="Книга", related_name="rating")

    def __str__(self):
        return f"{self.star} - {self.book}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        db_table = 'rating'
        app_label = 'testapp'

