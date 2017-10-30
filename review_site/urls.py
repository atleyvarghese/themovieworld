"""review_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                    document_root=settings.STATIC_ROOT)

admin.site.site_header = ('Movie World')
admin.site.index_title = ('Movie World')
admin.site.site_title = ('Admin')

