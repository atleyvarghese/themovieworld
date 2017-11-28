import tmdbsimple as tmdb
from celery import shared_task
import requests

from apps.review.models import MovieList, Movie, Genre, CastAndCrew, Role
import imdb


@shared_task
def collect_movie():
    """
        To List Movies based on genre
    """
    tmdb.API_KEY = '22ce6e6a848dfc0fd4376e55d8890949'
    obj = MovieList.objects.filter(collected=False)
    if obj:
        for movies in obj:
            id=str(movies.api_id)
            movie = tmdb.Movies(id)
            response = movie.info()
            imdb_id = movie.imdb_id
            imdb_id = int(imdb_id.replace("t", ""))
            ia = imdb.IMDb()
            imdb_object = ia.get_movie(imdb_id)
            url='https://image.tmdb.org/t/p/w500/'+movie.poster_path+'?api_key=22ce6e6a848dfc0fd4376e55d8890949'
            Movie.objects.create(title=movie.title,synopsis=movie.overview,rel_date=movie.release_date,
                                  image=url,popularity=movie.popularity,runtime=movie.runtime,imdb_rating=imdb_object['rating'])
            new=Movie.objects.last()
            if movie.genres:
                for item in movie.genres:
                    new.genre.add(Genre.objects.get(name=item['name']))
            reponse = movie.credits()
            for item in reponse['cast'][:4]:
                id = str(item['id'])
                f = requests.get("https://api.themoviedb.org/3/person/" + id + "?api_key=22ce6e6a848dfc0fd4376e55d8890949")
                data = f.json()
                if CastAndCrew.objects.filter(api_id=data['id']):
                    cast=CastAndCrew.objects.get(api_id=data['id'])
                else:
                    cast=CastAndCrew.objects.create(name=data['name'],api_id=data['id'],biography=data['biography'],
                                                popularity=data['popularity'])
                    if data['profile_path']:
                        url = "https://image.tmdb.org/t/p/w500/"+data['profile_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
                        cast.image = url
                    cast.save()
                role = Role.objects.create(role=item['character'],crew=cast,movie=new)
            for item in reponse['crew'][:10]:
                if item['job'] == 'Writer' or item['job'] == 'Director':
                    id = str(item['id'])
                    f = requests.get("https://api.themoviedb.org/3/person/" + id + "?api_key=22ce6e6a848dfc0fd4376e55d8890949")
                    data = f.json()
                    if CastAndCrew.objects.filter(api_id=data['id']):
                        cast=CastAndCrew.objects.get(api_id=data['id'])
                    else:
                        cast=CastAndCrew.objects.create(name=data['name'],api_id=data['id'],biography=data['biography'],
                                                    popularity=data['popularity'])
                        if data['profile_path']:
                            url = "https://image.tmdb.org/t/p/w500/"+data['profile_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
                            cast.image = url
                        cast.save()
                    role = Role.objects.create(role=item['job'],crew=cast,movie=new)
            response = movie.videos()
            new.video = movie.results[0]['key']
            response = movie.images()
            url = "https://image.tmdb.org/t/p/w1280/"+movie.backdrops[0]['file_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
            new.backdrop=url
            new.save()
            movies.collected=True
            movies.save()


@shared_task
def collect_a_movie(id):
    """
        To List Movies based on genre
    """
    tmdb.API_KEY = '22ce6e6a848dfc0fd4376e55d8890949'
    id=str(id)
    movie = tmdb.Movies(id)
    response = movie.info()
    imdb_id = movie.imdb_id
    imdb_id = int(imdb_id.replace("t", ""))
    ia = imdb.IMDb()
    imdb_object = ia.get_movie(imdb_id)
    url='https://image.tmdb.org/t/p/w500/'+movie.poster_path+'?api_key=22ce6e6a848dfc0fd4376e55d8890949'
    Movie.objects.create(title=movie.title,synopsis=movie.overview,rel_date=movie.release_date,
                        image=url,popularity=movie.popularity,runtime=movie.runtime,imdb_rating=imdb_object['rating'])
    movie_list = MovieList.objects.create(title=movie.title,api_id=id,collected=True)
    movie_list.save()
    new=Movie.objects.last()
    if movie.genres:
        for item in movie.genres:
            new.genre.add(Genre.objects.get(name=item['name']))
    reponse = movie.credits()
    for item in reponse['cast'][:4]:
        id = str(item['id'])
        f = requests.get("https://api.themoviedb.org/3/person/" + id + "?api_key=22ce6e6a848dfc0fd4376e55d8890949")
        data = f.json()
        if CastAndCrew.objects.filter(api_id=data['id']):
            cast=CastAndCrew.objects.get(api_id=data['id'])
        else:
            cast=CastAndCrew.objects.create(name=data['name'],api_id=data['id'],biography=data['biography'],
                                           popularity=data['popularity'])
            if data['profile_path']:
                url = "https://image.tmdb.org/t/p/w500/"+data['profile_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
                cast.image = url
                cast.save()
        role = Role.objects.create(role=item['character'],crew=cast,movie=new)
    for item in reponse['crew'][:10]:
        if item['job'] == 'Writer' or item['job'] == 'Director':
            id = str(item['id'])
            f = requests.get("https://api.themoviedb.org/3/person/" + id + "?api_key=22ce6e6a848dfc0fd4376e55d8890949")
            data = f.json()
            if CastAndCrew.objects.filter(api_id=data['id']):
                cast=CastAndCrew.objects.get(api_id=data['id'])
            else:
                cast=CastAndCrew.objects.create(name=data['name'],api_id=data['id'],biography=data['biography'],
                                            popularity=data['popularity'])
                if data['profile_path']:
                    url = "https://image.tmdb.org/t/p/w500/"+data['profile_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
                    cast.image = url
                    cast.save()
            role = Role.objects.create(role=item['job'],crew=cast,movie=new)
    response = movie.videos()
    new.video = movie.results[0]['key']
    response = movie.images()
    url = "https://image.tmdb.org/t/p/w1280/"+movie.backdrops[0]['file_path']+"?api_key=22ce6e6a848dfc0fd4376e55d8890949"
    new.backdrop=url
    new.save()
