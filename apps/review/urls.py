from django.conf.urls import url

from apps.review import views
from apps.review.views import MovieListView, MovieDetailView, SearchView, FavouriteView, GenreView, CategoryView

urlpatterns = [

    url(r'^$',MovieListView.as_view()),
    url(r'^(?P<slug>[\w-]+)$', MovieDetailView.as_view(), name='detail'),
    url(r'^collect/$', views.collect_movies,name='collect'),
    url(r'^favorites/$', views.favourite,),
    url(r'^search/$', SearchView.as_view(),name='search'),
    url(r'^favourite/$', FavouriteView.as_view()),
    url(r'^genre/(?P<slug>[\w-]+)/$', GenreView.as_view(),name='genre-view'),
    url(r'^category/(?P<category>\w+)/$', CategoryView.as_view(),name='category'),

]
