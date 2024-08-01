from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("home", views.home, name="home"),
    path('guest_login/', views.guest_login, name='guest_login'),
    path('contact/', views.contact, name='contact'),
    path('english_diagnostic/', views.english_diagnostic, name='english_diagnostic'),
    path('english_diagnostic_test/', views.english_diagnostic_test, name='english_diagnostic_test'),
    path('download-cv-eng/', views.download_cv_eng, name='download_cv_eng'),
    path('download-cv-esp/', views.download_cv_esp, name='download_cv_esp'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
