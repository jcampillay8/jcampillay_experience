from .views import RegistrationView, UsernameValidationView, EmailValidationView, RequestPasswordResetEmail, LogoutView, VerificationView, LoginView,CompletePasswordReset,CredentialsValidationView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
     
    path('set-new-password/<uidb64>/<token>',
         CompletePasswordReset.as_view(), name='reset-user-password'),
    path('request-password',RequestPasswordResetEmail.as_view(),name="request-password"),
    path('check_email', csrf_exempt(CredentialsValidationView.as_view()), name='validate-email'),
    path('check_username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
     

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)