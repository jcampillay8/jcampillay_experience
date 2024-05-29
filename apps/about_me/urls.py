from django.urls import path
from django.urls.conf import include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.about_me_home, name='about_me_home'),
    path('about_me/', views.about_me, name='about_me'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)