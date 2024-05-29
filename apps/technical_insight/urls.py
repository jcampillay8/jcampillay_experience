from django.urls import path
from django.urls.conf import include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.technical_insight, name='technical_insight'),
    path('knowledge_skills/', views.knowledge_skills, name='knowledge_skills'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)