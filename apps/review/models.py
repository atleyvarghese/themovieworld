from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Genre(models.Model):
    """
            Genre entries for movies
    """
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name',
                         unique_with=['id'],
                         unique=True, always_update=True)

    class Meta:
        verbose_name_plural = "Genre"

    def __str__(self):
        return self.name


class MovieList(models.Model):
    """
            Details about Movies added and to be added
    """
    title = title = models.CharField(_('Title'), max_length=200, null=True, blank=True)
    api_id = models.IntegerField()
    collected = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Movie List"
        verbose_name = "Movie List"


class CastAndCrew(models.Model):
    """
        Details about Cast And Crew
    """
    name = models.CharField(_('Name'), max_length=200)
    api_id = models.IntegerField()
    biography = models.TextField(_('Biography'), default='Biography yet to added',null=True, blank=True)
    image = models.URLField(_('Image'), null=True, blank=True)
    popularity=models.IntegerField(default=1,null=True, blank=True)
    slug = AutoSlugField(populate_from='name',
                         unique_with=['api_id'],
                         unique=True, always_update=True)

    class Meta:
        verbose_name_plural = "Cast And Crew"

    def __str__(self):
        return self.name



class Movie(models.Model):
    """
        Details about Movies
    """
    title = models.CharField(_('Title'), max_length=200)
    genre = models.ManyToManyField(Genre, blank=True)
    synopsis = models.TextField(_('Synopsis'), default='Synopsis yet to added')
    rel_date = models.DateField(default='2017-08-11')
    add_date = models.DateTimeField(auto_now_add=True)
    image = models.URLField(_('Image'), null=True, blank=True)
    video = models.CharField(_('Video'), null=True, blank=True, max_length=20)
    popularity=models.IntegerField(default=1)
    slug = AutoSlugField(populate_from='title',
                         unique_with=['title'],
                         unique=True, always_update=True)
    published = models.BooleanField(_('Published'), default=False)
    backdrop = models.URLField(_('Background'), null=True, blank=True)
    cast = models.ManyToManyField(CastAndCrew, through='Role',blank=True)

    class Meta:
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title


class Role(models.Model):
    """
            Details about Role and Movie associated
    """
    movie = models.ForeignKey(Movie)
    crew = models.ForeignKey(CastAndCrew,related_name='role_crew')
    role = models.CharField(_('Role'),max_length=200)

    class Meta:
        verbose_name_plural = "Role"

    def __str__(self):
        return self.role


class Favorites(models.Model):
    """
            Save favorites for each user
    """
    user=models.ForeignKey(User)
    list=models.ManyToManyField(Movie,blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Favorites"


