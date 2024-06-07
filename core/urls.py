from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import handler404
from apps.Error_handler.views import Error404View, Error505View

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("authentication/", include("apps.authentication.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include("apps.home.urls")),
    
    path('guest_user/', include('guest_user.urls')),
    path('about_me_home/', include('apps.about_me.urls')),
    path('technical_insight/', include('apps.technical_insight.urls')),
    path('Quizzes/', include("apps.Quizzes.urls")),
    path('blog/', include("apps.blog.urls")),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
)

handler404 = Error404View.as_view()

handler505 = Error505View.as_error_view()


# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("", include("apps.home.urls")),
#     path("authentication/", include("apps.authentication.urls")),
#     path('guest_user/', include('guest_user.urls')),
#     path('about_me_home/', include('apps.about_me.urls')),
#     path('technical_insight',include('apps.technical_insight.urls')),
#     path('Quizzes/',include("apps.Quizzes.urls")),
#     path('blog/',include("apps.blog.urls")),
#     path('django_plotly_dash/', include('django_plotly_dash.urls')),
#     path("i18n/", include("django.conf.urls.i18n")),
#     path("admin/", admin.site.urls),
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)