from django.urls import path
from django.urls.conf import include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.quiz_index, name='quiz_index'),
    path('quiz_post/', views.seeQuiz, name='quiz_post'),
    path('quiz_creation/', views.createQuiz, name='quiz_creation'),
    path('quiz_post/<int:pk>', views.seeQuiz, name='quiz_post'),
    # path('quiz_update/<int:pk>', views.updateQuiz, name='quiz_update'),
    path('quiz_delete/<int:pk>', views.deleteQuiz, name='quiz_delete'),
    # path('likes/<int:pk>', views.darLike, name='dar_like'),
    # path('quiz_gcp/<int:pk>', views.dash_view, name='quiz_gcp'),
    # path('test/<int:pk>', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)