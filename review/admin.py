from django.contrib import admin
from review.models import Genre, Movies, Movie_List, favorites


def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Mark selected Movies as published"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = "Mark selected Movies as unpublished"

def collected(modeladmin, request, queryset):
    queryset.update(collected=True)
collected.short_description = "Mark selected Movies as collected"

def uncollected(modeladmin, request, queryset):
    queryset.update(collected=False)
uncollected.short_description = "Mark selected Movies as not collected"


class MoviesAdmin(admin.ModelAdmin):
    actions = [make_published,make_unpublished]
    search_fields = ['title']


class Movies_listAdmin(admin.ModelAdmin):
    actions = [collected,uncollected]
    search_fields = ['title']



admin.site.register(Movies,MoviesAdmin)
admin.site.register(Genre)
admin.site.register(Movie_List,Movies_listAdmin)
admin.site.register(favorites)


