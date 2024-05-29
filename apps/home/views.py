import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from guest_user.decorators import allow_guest_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from functools import wraps
from django.contrib.auth.models import AnonymousUser
from django.views.generic import (View, TemplateView)
#from apps.contact.forms import ContactForm
from .forms import ContactForm
import traceback
from django.utils.translation import gettext as _


class GuestUser:
    is_guest = True
    is_authenticated = False
    is_anonymous = False


def login_or_guest_required(func):
    @wraps(func)
    def decorated_view(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser) and not request.session.get('is_guest', False):
            return redirect('welcome')  # Redirigir a todos los usuarios anónimos que no son invitados a 'welcome'
        if request.user.is_authenticated:
            return login_required(login_url='/authentication/login')(func)(request, *args, **kwargs)
        elif request.session.get('is_guest', False):
            return allow_guest_user(func)(request, *args, **kwargs)
        else:
            return redirect('/authentication/login')
    return decorated_view


def guest_login(request):
    request.session['is_guest'] = True  # Establecer una variable de sesión para indicar que el usuario es un invitado
    return redirect('home')  # Redirigir al usuario a la página de inicio


@login_or_guest_required
def home(request):

    contact_form = ContactForm(request.POST or None)
    

    context = {
        'current_page': 'welcome',  # Cambia esto por el nombre de tu página
        'form':contact_form,
    }
    # Si el usuario no está autenticado o no es un invitado, redirigir a 'welcome'
    if not request.user.is_authenticated and not request.user.is_guest:

        return redirect('welcome',{ 'current_page': 'welcome','form':contact_form})

    return render(request, 'home/home.html',{ 'current_page': 'welcome','form':contact_form})


def welcome(request):
    if request.user.is_authenticated and not request.session.get('is_guest', False):
        return redirect('home')

    # Crear el contexto con los datos cargados
    context = {
        
        'current_page': 'welcome',
    }
    return render(request, 'partials/_welcome_content.html', context)






