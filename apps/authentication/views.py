from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.views import View
import json
from django.views.generic import (View, TemplateView)
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext as _


import threading
# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': -('Email is invalid')}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': -('sorry email in use,choose another one ')}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username', '')
        if not str(username).isalnum():
            return JsonResponse({'error': _('username can  only contain letters and numbers')})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': _('username is taken,please choose a new one')})
        return JsonResponse({'is_available': 'true'})



class CredentialsValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email', '')
        if not email:
            return JsonResponse({'error': _('Please enter an email')})
        is_valid = validate_email(email)
        if not is_valid:
            return JsonResponse({'error': _('Please enter a valid email')})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': _('Email is taken,please choose a new one')})

        return JsonResponse({'valid': True})

class RegistrationView(View):
    def get(self, request):
        
        context = {
            'current_page': 'register'
        }
        
        return render(request, 'authentication/register.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        

        context = {
            'current_page': 'register'
        }

        if first_name and last_name and username and email and password:  # Asegúrate de que también se proporcionó el nombre de la compañía
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password) < 6:
                        messages.error(request, _('Password too short'))
                        return render(request, 'authentication/register.html', context)

                    # Crea el usuario e incluye first_name y last_name
                    user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name)
                    user.set_password(password)
                    user.is_active = False
                    user.is_staff = False
                    user.save()

                    # Asignar al usuario al grupo "Empresa_Cliente"

                    current_site = get_current_site(request)
                    email_body = {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }

                    link = reverse('activate', kwargs={
                                    'uidb64': email_body['uid'], 'token': email_body['token']})

                    email_subject = _('Activate your account')

                    activate_url = 'http://'+current_site.domain+link

                    email = EmailMessage(
                        email_subject,
                        _('Hi ')+user.username + _(', Please the link below to activate your account \n')+activate_url,
                        'noreply@semycolon.com',
                        [email],
                    )
                    EmailThread(email).start()
                    messages.success(request, _('Se le ha enviado un correo a su cuenta con un enlace de validación. Por favor, acceda a su correo y haga clic en el enlace para validar y activar su cuenta'))
                    return render(request, 'authentication/register.html',context)

        else:
            messages.error(request, _('Please fill all fields'))
            return render(request, 'authentication/register.html',context)





class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect(_('login')+_('?message=')+_('User already activated'))

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, _('Account activated successfully'))
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        
        context = {
            'current_page': 'login'
        }
        
        return render(request, 'authentication/login.html', context)

    def post(self, request):
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Actualizar el idioma seleccionado en la sesión
        

        context = {
            'current_page': 'login'
        }  

        if username_or_email and password:
            # Intenta autenticar por nombre de usuario
            user = auth.authenticate(username=username_or_email, password=password)
            
            # Si la autenticación por nombre de usuario falla, intenta por correo electrónico
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = auth.authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user:
                if user.is_active:
                    auth.login(request, user)
                    #messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                    return redirect('home')
                messages.error(request, _('Account is not active, please check your email'))
                return render(request, 'authentication/login.html')
            messages.error(request, _('Invalid credentials, try again'))
            return render(request, 'authentication/login.html', context)
        else:
            messages.error(request, _('Please fill all fields'))
            return render(request, 'authentication/login.html', context)




class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, _('You have been logged out'))
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):

        context = {
            'current_page': _('forgot_password')
        }
        return render(request, 'authentication/reset-password.html', context)

    def post(self, request):
        email = request.POST.get('email')

        # Actualizar el idioma seleccionado en la sesión
        
        context = {
            'current_page': _('forgot_password')
        }

        if email is not None:
            if not validate_email(email):
                messages.error(request,_('Please supply a valid email'))
                return render(request,'authentication/reset-password.html',context)
        else:
            # Manejar el caso cuando email es None
            messages.error(request, _('El campo de correo electrónico es obligatorio.'))
            return render(request, 'authentication/reset-password.html', context)

        current_site = get_current_site(request)
        user=User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                            'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = _('Password reset Instrucctions')

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                _('Hi there, Please the link below to reset your password \n')+reset_url,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()
            messages.success(request,_('I have sent you an email to reset your password'))

        return render(request,'authentication/reset-password.html',context)

    # def get_context(self, request):

    #     context = {
    #         'selected_language': request.language_data
    #         #'fieldValues': request.POST,
    #     }

    #     return context


        
class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request, _('Password link is invalid, please request a new one'))
                return render(request,'authentication/reset-password.html')
        
        except Exception as identifier:
            pass
        return render(request,'authentication/set-new-password.html',context)
    
    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }

        password=request.POST['password']
        password2=request.POST['password2']

        if password != password2:
            messages.error(request,_('Password do not match'))
            return render(request,'authentication/set-new-password.html',context)
        
        if len(password)< 6:
            messages.error(request,_('Password too short'))
            return render(request,'authentication/set-new-password.html',context)   

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)  # Aquí está la corrección
            user.save()

            messages.success(request,_('Password reset successfuly you can login now with your new password'))
            return redirect('login')
        except Exception as identifier:
            messages.info(request,_('Something went wrong, try again'))
            return render(request,'authentication/set-new-password.html',context)

        


        #return render(request,'authentication/set-new-password.html',context)