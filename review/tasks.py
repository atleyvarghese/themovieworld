import tmdbsimple as tmdb
from celery import shared_task

from review.models import Movie_List, Movies, Genre


@shared_task
def collect_movie():
    """
        To List Movies based on genre
    """
    tmdb.API_KEY = '22ce6e6a848dfc0fd4376e55d8890949'
    obj = Movie_List.objects.filter(collected=False)
    if obj:
        for movies in obj:
            id=str(movies.api_id)
            movie = tmdb.Movies(id)
            response = movie.info()
            url='https://image.tmdb.org/t/p/w500/'+movie.poster_path+'?api_key=22ce6e6a848dfc0fd4376e55d8890949'
            Movies.objects.create(title=movie.title,synopsis=movie.overview,rel_date=movie.release_date,
                                  image=url,popularity=movie.popularity)
            new=Movies.objects.last()
            if movie.genres:
                for item in movie.genres:
                    new.genre.add(Genre.objects.get(name=item['name']))
            response = movie.videos()
            url="https://www.youtube.com/embed/"+movie.results[0]['key']
            new.video = url
            response = movie.images()
            url = "https://image.tmdb.org/t/p/w1280/"+movie.backdrops[0]['file_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
            new.backdrop=url
            new.save()
            movies.collected=True
            movies.save()
