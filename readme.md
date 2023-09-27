## **Это было так наивно и смешно...**
*Разработка пришлась на период, когда еще был интерес к Django/DRF\
и начинался интерес к фронту на JS, к CSS, с параллельной попыткой посмотреть, что такое nginx.\
Очень много недоделок, наивный ванильный фронтенд.\
Данные по книгам брались парсингом rss с сайта kodges (ныне сайт не работает)\
Если дорабатывать, то под Докер с переменными окружения,  фронт на Vue.JS 3, бэк на Django 4, добавить gunicorn для продакшена*

*Нужна доработка функционалов авторизации, пагинации с возможностью выбора на фронте кол-ва объектов на странице (бэк это уже знает),*  
*рейтингов, отзывов, допилить nginx с отработкой страниц 404 и 500.*

#### **Inspired by DjangoSchool**
* Посмотрел на DATABASE_ROUTER, DRF, Paginator, Queryset, Filtering
* в проекте отдельная база под данные книг и отдельная под нужды Django
* БД книг не пополняется, но задумка была - при открытии сайта делать выборку\
  по категориям книг и в боковом меню выстраивать категории по количеству книг по убыванию
* Также можно посмотреть, какие книги были добавлены на конкретную дату с группировкой по категориям
* Реализован поиск
* Реализована пагинация на бэке и обработка на фронтенде
* в репозиторий естественно не включена папка с media, там овер 1Гб обложек книг.


RUN PROJECT:

0) In django shell you should generate and put to settings.py new SECRET_KEY: \
*from django.core.management.utils import get_random_secret_key*  \
*print(get_random_secret_key())*

1) In project root dir: \
$ source /venv/Scripts/activate

2) In project root dir: \
$ cd django_book/
(venv)

3) In project dir: \/django_book \
$ python manage.py runserver

4) run \
start /django_book/nginx

5) Run browser and navigate to 127.0.0.1

---

* *filtering*  \
GET /api/v1/first5/?year_min=2019&year_max=2021 \
GET /api/v1/first5/?rubrics=%D0%90%D1%83%D0%B4&title=&year_min=&year_max=

////
// Frontend's links
////
* *get last 5 dates or 5 dates before <user_date>, nearest date to <user_date>, 5 dates after <user_date>* \
GET /api/v1/dates/

* *get books by categories by user_date (2021-08-08)*  \
GET /api/v1/listbydate/?date=${dateText}

* *get rubrics with book's count*  \
GET /api/v1/rubrics

* *get books by rubric's id* \
GET /api/v1/rubrics/<int:id>/

* *get service info and books of rubric <id> with navigation info (books per page = <user_size> or 10)!!!!* \
GET /api/v1/rubrics/1/?size=<user_size>&page=3

* *searching (return array or empty)* \
GET /api/v1/search/?title=vascript&year_min=2019
