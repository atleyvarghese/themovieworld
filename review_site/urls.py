from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from review_site import settings

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^',include('review.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                    document_root=settings.STATIC_ROOT)

admin.site.site_header = ('Movie World')
admin.site.index_title = ('Movie World')
admin.site.site_title = ('Admin')

