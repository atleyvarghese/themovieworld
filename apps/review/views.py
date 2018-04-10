from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, FormView

from apps.review.forms import SearchForm
from apps.review.models import Movie, Favorites, Genre, CastAndCrew
from .tasks import collect_movie, collect_a_movie


class MovieListView(ListView):
    """
        To List Movies
    """
    model = Movie
    template_name = 'review/index.html'
    paginate_by = 16
    context_object_name = 'movies'
    queryset = Movie.objects.all().order_by('-rel_date')[:10]

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['type'] = _('Latest')
        context['title'] = _('Movies')
        context['popular'] = Movie.objects.all().order_by('-popularity')[:10]
        return context


class MovieDetailView(DetailView):
    """
    To display Movie in detail
    """
    model = Movie
    template_name = 'review/details.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        get_slug = self.kwargs['slug']
        movie = Movie.objects.get(slug=get_slug)
        context['movie'] = movie
        context['genres'] = Genre.objects.all()
        if self.request.user.is_authenticated:
            if Favorites.objects.filter(user_id=self.request.user.id).exists():
                obj = Favorites.objects.filter(user__id=self.request.user.id)
                if obj[0].list.filter(slug=self.kwargs['slug']).exists():
                    context['fav'] = True
            else:
                context['fav']=False
        else:
            context['fav'] = False
        context['cast'] = movie.cast.all()
        context['roles'] = movie.role_set.all()
        context['roles1'] = list(zip(context['cast'],context['roles']))
        obj = Movie.objects.get(slug=get_slug)
        context['title'] = obj.title
        return context


class PeopleDetailView(DetailView):
    """
    To display Movie in detail
    """
    model = CastAndCrew
    template_name = 'review/people_detail.html'
    context_object_name = 'people'

    def get_context_data(self, **kwargs):
        context = super(PeopleDetailView, self).get_context_data(**kwargs)
        people = CastAndCrew.objects.get(slug=self.kwargs['slug'])
        context['people'] = people
        context['title'] = people.name
        context['flim'] = Movie.objects.filter(cast__slug=self.kwargs['slug'])
        return context



def collect_movies(request):
    """
        To call celery to perform api call for uncollected movies in Movie_List model
    """
    collect_movie.delay()
    return HttpResponse('')


def collect_a_movie_data(request):
    """
        To call celery to perform api call for uncollected movies in Movie_List model
    """
    # import pdb
    # pdb.set_trace()
    if request.GET.get('id'):
    # id = 12445
        collect_a_movie.delay(request.GET.get('id'))
    return HttpResponse("")


def favourite(request):
    """
        Function check whether a movie is added to favourite and add it to favourite when clicked
    """
    status = {}
    if Favorites.objects.filter(user_id=request.user.id).exists():
        favorite=Favorites.objects.filter(user__id=request.user.id)
        if favorite[0].list.filter(id=request.GET.get('id')).exists():
            favorite[0].list.remove(Movie.objects.get(id=int(request.GET.get('id'))))
            status['status'] = 0
            return JsonResponse(status)
        else:
            favorite[0].list.add(Movie.objects.get(id=int(request.GET.get('id'))))
            status['status'] = 1
            return JsonResponse(status)
    else:
        favorite=Favorites.objects.create(user_id=request.user.id)
        favorite.list.add(Movie.objects.get(id=int(request.GET.get('id'))))
        favorite.save()
        status['status'] = 1
        return JsonResponse(status)


class SearchView(ListView):
    """
            for users to search for Movies based on Movie name, Genre, Latest, Oldest
    """
    template_name = 'review/search1.html'
    context_object_name = 'movies'
    paginate_by = 8

    def get_queryset(self,**kwargs):
        # import pdb
        # pdb.set_trace()
        movies = Movie.objects.all()
        if self.request.GET.getlist('genre'):
            genre_list = self.request.GET.getlist('genre')
            for x in genre_list:
                movies = movies.filter(genre__name=x)
        if self.request.GET.get('q'):
            movies = movies.filter(title__icontains=self.request.GET.get('q'))
        if self.request.GET.get('rating'):
            movies = movies.filter(imdb_rating__gte=self.request.GET.get('rating'))
        if self.request.GET.get('sort'):
            return movies.order_by(self.request.GET.get('sort'))
        return movies.order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['title'] = _('Search')
        context['count'] = self.get_queryset().count()
        if self.request.GET.get('q'):
            context['q'] = self.request.GET.get('q')
        if self.request.GET.get('rating'):
            context['rating'] = int(self.request.GET.get('rating'))
        else:
            context['rating'] = 1
        if self.request.GET.get('sort'):
            context['sort'] = self.request.GET.get('sort')
        else:
            context['sort'] = 'rel_date'
        return context

class SearchView1(ListView):
    model = Movie
    template_name = 'review/results.html'
    context_object_name = 'results'
    paginate_by = 6

    def get_queryset(self, **kwargs):
        movies = Movie.objects.all()
        if self.request.GET.getlist('genre'):
            genre_list = self.request.GET.getlist('genre')
            for x in genre_list:
                movies = movies.filter(genre__name=x)
        if self.request.GET.get('q'):
            movies = movies.filter(title__icontains=self.request.GET.get('q'))
        if self.request.GET.get('rating'):
            movies = movies.filter(imdb_rating__gte=self.request.GET.get('rating'))
        return movies.order_by('-rel_date')



class FavouriteView(ListView):
    """
        To display favourite movies for authenticated user
    """
    model = Favorites
    template_name = 'review/fav.html'
    paginate_by = 9
    context_object_name = 'movies'

    def get_queryset(self):
        if Favorites.objects.filter(user_id=self.request.user.id).exists():
            favorite=Favorites.objects.get(user_id=self.request.user.id)
            return favorite.list.all().order_by('-rel_date')
        else:
            favorite = Favorites.objects.create(user_id=self.request.user.id)
            favorite.save()
            return favorite.list.all().order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(FavouriteView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['type'] = _('My Favorite')
        context['title'] = _('Favorites')
        return context


class GenreView(ListView):
    """
        To List Movies based on genre
    """
    model = Movie
    template_name = 'review/home.html'
    paginate_by = 9
    context_object_name = 'movies'

    def get_queryset(self, **kwargs):
        slug = self.kwargs['slug']
        return Movie.objects.filter(genre__slug=slug).order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        movie = Genre.objects.get(slug=self.kwargs['slug'])
        context['type'] = movie.name
        context['title'] = movie.name
        return context


class CategoryView(ListView):
    """
        To List Movies based on Category
    """
    model = Movie
    template_name = 'review/home.html'
    paginate_by = 6
    context_object_name = 'movies'

    def get_queryset(self, **kwargs):
        category = self.kwargs['category']
        if category == 'latest':
            return Movie.objects.all().order_by('-rel_date')[:9]
        else:
            return Movie.objects.all().order_by('-popularity')

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        category = self.kwargs['category']
        if category == 'latest':
            context['type'] = _('Latest')
            context['title'] = _('Latest Movies')
        else:
            context['type'] = _('Popular')
            context['title'] = _('Popular Movies')
        return context





