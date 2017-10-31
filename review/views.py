from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView

from review.models import Movies, favorites, Genre
from .tasks import collect_movie


class MovieListView(ListView):
    """
        To List Movies
    """
    model = Movies
    template_name = 'home.html'
    paginate_by = 9
    context_object_name = 'movies'
    queryset = Movies.objects.all().order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['type'] = 'Latest'
        context['title'] = 'Movies'
        return context


class MovieDetailView(DetailView):
    """
    To display Movie in detail
    """
    model = Movies
    template_name = 'detail.html'
    context_object_name = 'Movie'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        get_slug = self.kwargs['slug']
        context['movie'] = Movies.objects.get(slug=get_slug)
        context['genres'] = Genre.objects.all()
        if self.request.user.is_authenticated:
            if favorites.objects.filter(user_id=self.request.user.id).exists():
                obj = favorites.objects.filter(user__id=self.request.user.id)
                if obj[0].list.filter(slug=self.kwargs['slug']).exists():
                    context['fav'] = True
            else:
                context['fav']=False
        else:
            context['fav'] = False
        obj = Movies.objects.get(slug=get_slug)
        context['title'] = obj.title
        return context



def collect_movies(request):
    """
        To call celery to perform api call for uncollected movies in Movie_List model
    """
    collect_movie.delay()
    return HttpResponse()


def favourite(request):
    """
        Function check whether a movie is added to favourite and add it to favourite when clicked
    """
    status = {}
    if favorites.objects.filter(user_id=request.user.id).exists():
        favorite=favorites.objects.filter(user__id=request.user.id)
        if favorite[0].list.filter(id=request.GET.get('id')).exists():
            favorite[0].list.remove(Movies.objects.get(id=int(request.GET.get('id'))))
            status['status'] = 0
            return JsonResponse(status)
        else:
            favorite[0].list.add(Movies.objects.get(id=int(request.GET.get('id'))))
            status['status'] = 1
            return JsonResponse(status)
    else:
        favorite=favorites.objects.create(user_id=request.user.id)
        favorite.list.add(Movies.objects.get(id=int(request.GET.get('id'))))
        favorite.save()
        status['status'] = 1
        return JsonResponse(status)


class SearchView(ListView):
    """
            for users to search for Movies based on Movie name, Genre, Latest, Oldest
    """
    model = Movies
    paginate_by = 6
    template_name = 'search.html'
    context_object_name = 'movies'

    def get_queryset(self,**kwargs):
        if 'order' in self.request.GET:
            if self.request.GET['order']=='Latest':
                order='-rel_date'
            else:
                order = 'rel_date'
            if self.request.GET['genre']=='All':
                return Movies.objects.filter(
                        Q(title__icontains=self.request.GET['name'])).order_by(order)
            else:
                return Movies.objects.filter(genre__name=self.request.GET['genre']).filter(
                        Q(title__icontains=self.request.GET['name'])).order_by(order)
        else:
            return Movies.objects.all().order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['title'] = 'Search'
        return context


class FavouriteView(ListView):
    """
        To display favourite movies of authenticated user
    """
    model = favorites
    template_name = 'home.html'
    paginate_by = 9
    context_object_name = 'movies'

    def get_queryset(self):
        if favorites.objects.filter(user_id=self.request.user.id).exists():
            favorite=favorites.objects.get(user_id=self.request.user.id)
            return favorite.list.all().order_by('-rel_date')
        else:
            favorite = favorites.objects.create(user_id=self.request.user.id)
            favorite.save()
            return favorite.list.all().order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(FavouriteView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['type'] = 'My Favorite'
        context['title'] = 'Favorites'
        return context


class GenreView(ListView):
    """
        To List Movies based on genre
    """
    model = Movies
    template_name = 'home.html'
    paginate_by = 9
    context_object_name = 'movies'

    def get_queryset(self, **kwargs):
        pk = self.kwargs['pk']
        return Movies.objects.filter(genre__id=pk).order_by('-rel_date')

    def get_context_data(self, **kwargs):
        context = super(GenreView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        movie = Genre.objects.get(id=self.kwargs['pk'])
        context['type'] = movie.name
        context['title'] = movie.name
        return context


class CategoryView(ListView):
    """
        To List Movies based on Category
    """
    model = Movies
    template_name = 'home.html'
    paginate_by = 6
    context_object_name = 'movies'

    def get_queryset(self, **kwargs):
        category = self.kwargs['category']
        if category=='latest':
            return Movies.objects.all().order_by('-rel_date')[:9]
        else:
            return Movies.objects.all().order_by('-popularity')

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        category = self.kwargs['category']
        if category == 'latest':
            context['type'] = 'Latest'
            context['title'] = 'Latest Movies'
        else:
            context['type'] = 'Popular'
            context['title'] = 'Popular Movies'
        return context





