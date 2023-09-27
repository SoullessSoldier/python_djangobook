from django.urls import path, include
from . import views
urlpatterns = [
    path('first5/', views.BooksListView.as_view()),
    #path('listbydate/', views.BooksLastListView.as_view()),
    path('listbydate/', views.BooksByRubricView4.as_view()),
    path('last3/', views.BooksByRubricView3.as_view()),
    path('last2/', views.BooksByRubricView2.as_view()),
    path('last1/', views.BooksByRubricView1.as_view()),
    path('last/', views.BooksByRubricView.as_view()),
    path('book/<int:pk>/', views.BookDetailView.as_view()),
    path('favorite/', views.FavoriteView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('rubrics/<int:id>/', views.RubricsBooksView.as_view()),
    path('rubrics/', views.RubricsCountView.as_view()),
    path('dates/', views.DatesLast5View.as_view()),
    path('search/', views.SearchListView.as_view()),
]