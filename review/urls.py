from django.conf.urls import url

from review import views
from review.views import MovieListView, MovieDetailView, SearchView, FavouriteView

urlpatterns = [

    url(r'^$',MovieListView.as_view()),
    url(r'(?P<slug>[\w-]+)$', MovieDetailView.as_view(), name='detail'),
    url(r'^collect/$', views.collect_movies,name='collect'),
    url(r'^favorites/$', views.favourite,),
    url(r'^search/$', SearchView.as_view(),name='search'),
    url(r'^favourite/$', FavouriteView.as_view(), ),
]
