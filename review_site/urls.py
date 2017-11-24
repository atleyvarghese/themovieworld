from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve

from review_site import settings

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account/', include('apps.accounts.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^',include('apps.review.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]

urlpatterns += [url(r'^media/(?P<path>.*)$', serve,
                   {'document_root': settings.MEDIA_ROOT, }),
               url(r'', include('django.contrib.staticfiles.urls')),]
admin.site.site_header = ('Movie World')
admin.site.index_title = ('Movie World')
admin.site.site_title = ('Admin')

