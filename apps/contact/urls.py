from django.urls import path
from django.urls.conf import include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.contact_home, name='contact_home'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)