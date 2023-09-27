RUN PROJECT:

1) AAA@DESKTOP-D61SGAA MINGW64 /c/coding/python/DjangoSchool-drf/django_book
$ source c:/coding/python/DjangoSchool-drf/venv/Scripts/activate

2) AAA@DESKTOP-D61SGAA MINGW64 /c/coding/python/DjangoSchool-drf
$ cd django_book/
(venv)

3) AAA@DESKTOP-D61SGAA MINGW64 /c/coding/python/DjangoSchool-drf/django_book
$ python manage.py runserver

4) start from FAR  c:/coding/python/DjangoSchool-drf/django_book/nginx ()

5) browser 127.0.0.1

---

https://youtu.be/oxHqBGZNWfA
filters https://youtu.be/0Pn-gzcVBAA --- фильтрация фильмов по годам и жанрам - django rest framework урок 10
djoser регистрация, авторизация, отправка email с подтверждением https://youtu.be/PC0S1dkRNtg
drf permissions jwt https://youtu.be/Svs3eCAvBaA
почитать www.django-rest-framework.org/api-guide/filtering
Вы должны не через GET-запрос обновлять данные а через PUT или PATCH
https://www.django-rest-framework.org/api-guide/serializers/
https://overcoder.net/q/1881625/drf-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BE%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8B%D1%85-%D0%BF%D0%BE%D0%BB%D0%B5%D0%B9-%D0%B2-%D0%B1%D0%B0%D0%B7%D0%B5-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85

filtering
GET /api/v1/first5/?year_min=2019&year_max=2021
GET /api/v1/first5/?rubrics=%D0%90%D1%83%D0%B4&title=&year_min=&year_max=

////
// Frontend's links
////
get last 5 dates or 5 dates before <user_date>, nearest date to <user_date>, 5 dates after <user_date> 
GET /api/v1/dates/

get books by categories by user_date (2021-08-08)
GET /api/v1/listbydate/?date=${dateText}

get rubrics with book's count
GET /api/v1/rubrics

get books by rubric's id
GET /api/v1/rubrics/<int:id>/

get service info and books of rubric <id> with navigation info (books per page = <user_size> or 10)!!!!
http://127.0.0.1:8000/api/v1/rubrics/1/?size=<user_size>&page=3

searching (return array or empty)
http://127.0.0.1:8000/api/v1/search/?title=vascript&year_min=2019