
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import logout_user



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.LoginView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='index.html'), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^home/', include('home.urls'), name="home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)