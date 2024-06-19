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
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
import os
from django.utils.translation import get_language
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
from django.http import FileResponse



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

    context['LANGUAGE_CODE'] = get_language()
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


def send_email_new(user, user_email, message_sent):
    name = user.get_full_name() if user.is_authenticated else user_email.split('@')[0]
    
    subject = "Gracias por su Interés: Pronto Me Pondré en Contacto"
    message = f"""
    Estimado(a) {name},

    Me complace informarle que su solicitud de contactarme ha sido generada y enviada con éxito. Agradezco su interés en mis habilidades y servicios. Siempre me esfuerzo por cumplir con las expectativas y dar lo mejor de mí.

    Pronto me pondré en contacto con usted para estar a su disposición. Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto conmigo.

    Saludos cordiales,

    Jaime Campillay Rojas
    Ingeniero en Aplicaciones Web y Consultor de Automatización de Procesos

    *** Su Mensaje ***
    {message_sent}
    """

    email = EmailMessage(
        subject,
        message,
        "no-contestar@inbox.mailtrap.io",
        [user_email],
        reply_to=[user_email],
    )
    
    email.send(fail_silently=False)



def fetch_resources(uri, rel):
    path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    
    # If the file is not found in STATIC_ROOT, check in STATICFILES_DIRS
    if not os.path.isfile(path):
        for static_dir in settings.STATICFILES_DIRS:
            alternative_path = os.path.join(static_dir, uri.replace(settings.STATIC_URL, ""))
            if os.path.isfile(alternative_path):
                return alternative_path
        raise Exception(f"El archivo {path} no existe.")
    
    return path

def send_email_with_pdf(user, user_email, message_sent, pdf, language):
    name = user.get_full_name() if user.is_authenticated else user_email.split('@')[0]
    
    if language == 'english':
        subject = "Thank you for Your Interest: I Will Get in Touch Soon"
        message = f"""
        Dear {name},

        I am pleased to inform you that your request to contact me has been successfully generated and sent. I appreciate your interest in my skills and services. I always strive to meet expectations and give my best.

        I will get in touch with you soon to make myself available. If you have any questions or need further information, please feel free to contact me.

        Best regards,

        Jaime Campillay Rojas
        Web Applications Engineer and Process Automation Consultant

        *** Your Message ***
        {message_sent}
        """
    elif language == 'spanish':
        subject = "Gracias por su Interés: Pronto Me Pondré en Contacto"
        message = f"""
        Estimado(a) {name},

        Me complace informarle que su solicitud de contactarme ha sido generada y enviada con éxito. Agradezco su interés en mis habilidades y servicios. Siempre me esfuerzo por cumplir con las expectativas y dar lo mejor de mí.

        Pronto me pondré en contacto con usted para estar a su disposición. Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto conmigo.

        Saludos cordiales,

        Jaime Campillay Rojas
        Ingeniero en Aplicaciones Web y Consultor de Automatización de Procesos

        *** Su Mensaje ***
        {message_sent}
        """

    email = EmailMessage(
        subject,
        message,
        "no-contestar@inbox.mailtrap.io",
        [user_email],
        reply_to=[user_email],
    )
    
    email.attach("Jaime_Campillay_Curriculum.pdf", pdf, "application/pdf")
    email.send(fail_silently=False)


def generate_pdf_from_template(template_path, context_dict):
    template = get_template(template_path)
    html_content = template.render(context_dict)
    
    pdf_file = HTML(string=html_content).write_pdf()
    return pdf_file

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        language = request.POST.get('language')  # Obtener el idioma seleccionado

        try:
            user = request.user if request.user.is_authenticated else None

            # Determinar la ruta de la plantilla según el idioma seleccionado
            if language == 'english':
                template_path = 'home/jcampillay_cv_eng.html'
            elif language == 'spanish':
                template_path = 'home/jcampillay_cv_esp.html'
            else:
                # Si no se selecciona un idioma válido, usar una plantilla predeterminada
                template_path = 'home/jcampillay_cv.html'

            # Generar el PDF desde la plantilla HTML
            context = {'name': name, 'email': email, 'message': message}

            # Agregar la ruta de la imagen al contexto
            image_path = os.path.abspath('core/assets/img/qr_website.png')
            context['qr_image'] = image_path

            pdf = generate_pdf_from_template(template_path, context)

            if pdf:
                send_email_with_pdf(user, email, message, pdf, language)
                messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
            else:
                messages.error(request, 'Hubo un error al generar el PDF.')

        except Exception as e:
            messages.error(request, f'Hubo un error al enviar tu mensaje: {str(e)}')

        #return render(request, 'contact/contact_home.html',{'current_page','contact_home'})
        return redirect('home')

    return render(request, "home/home.html", {'current_page': 'home'})




def generate_pdf_from_template(template_path, context_dict, output_path=None):
    try:
        # Renderizar la plantilla HTML con el contexto
        template = get_template(template_path)
        html_content = template.render(context_dict)

        # Crear el archivo PDF usando WeasyPrint
        pdf_file = HTML(string=html_content).write_pdf()

        if output_path:
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        else:
            return pdf_file

    except Exception as e:
        return HttpResponseServerError(str(e))


def download_cv(request, template_name):
    if template_name == 'jcampillay_cv_eng':
        template_path = 'home/jcampillay_cv_eng.html'
    elif template_name == 'jcampillay_cv_esp':
        template_path = 'home/jcampillay_cv_esp.html'
    else:
        return HttpResponseServerError('Invalid template name')

    # Agregar la ruta de la imagen QR al contexto
    qr_image_path = os.path.abspath('core/assets/img/qr_website.png')
    context = {'qr_image': qr_image_path}  # Agrega cualquier otro contexto necesario para la plantilla

    # Ruta de salida para el PDF
    output_path = os.path.join(settings.MEDIA_ROOT, f'{template_name}.pdf')

    # Generar y guardar el PDF desde la plantilla
    generate_pdf_from_template(template_path, context, output_path)

    # Devolver el PDF como respuesta
    return FileResponse(open(output_path, 'rb'), content_type='application/pdf')


def download_cv_eng(request):
    return download_cv(request, 'jcampillay_cv_eng')

def download_cv_esp(request):
    return download_cv(request, 'jcampillay_cv_esp')
