from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.views.generic import (View, TemplateView)
from django.views.decorators.csrf import csrf_exempt
from apps.list_manager.models import AsuntoCorreo, DestinatarioCorreo, ConCopiaCorreo, TipoActividad, CategoriaRequerimiento
import traceback
import threading
import pdfkit

from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import os
from weasyprint import HTML

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

def obtener_asunto_correo():
    try:
        # Obtener el único registro de AsuntoCorreo
        asunto_correo = AsuntoCorreo.objects.get()
        return asunto_correo
    except AsuntoCorreo.DoesNotExist:
        # Si no se encuentra ningún registro
        return None

def obtener_destinatarios_cc():
    try:
        destinatarios_cc = ConCopiaCorreo.objects.values_list('direccion_con_copia', flat=True)  # Obtener una lista de correos electrónicos en copia
        return destinatarios_cc
    except ConCopiaCorreo.DoesNotExist:
        return []

def send_email_new(user, user_email,message_sent):
    name = user.get_full_name()  # Suponiendo que tienes un método para obtener el nombre completo del usuario
    
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


# def send_email_new_request(user_email,result):

#     subject = "Solicitud Nuevos Requerimientos DTS Enviada Exitosamente"

#     message = """
#     Estimado cliente,

#     Nos complace informarle que su solicitud de cotización ha sido generada y enviada con éxito. Agradecemos su confianza en nuestros servicios y nos esforzamos por cumplir con sus expectativas.

#     Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto con nosotros. Estamos a su disposición para ayudarle.

#     Saludos cordiales,

#     DTS Automatizaciones
#     """
#     email = EmailMessage(
#         subject,
#         message,
#         "no-contestar@inbox.mailtrap.io",
#         [user_email],
#         reply_to=[user_email],
#         cc=obtener_destinatarios_cc()  # Agregar los destinatarios en copia obtenidos de ConCopiaCorreo
#     )
#     # Adjuntar la imagen
#     email.attach_file('core/assets/images/logo/DTS_logo_admin.png')
    
#     email.send(fail_silently=False)





# @login_required
# @csrf_exempt
# def contact(request):
#     contact_form = ContactForm()

#     if request.method == "POST":
#         contact_form = ContactForm(data=request.POST)
#         if contact_form.is_valid():
#             name = contact_form.cleaned_data.get('name')
#             last_name = contact_form.cleaned_data.get('last_name')
#             phone = contact_form.cleaned_data.get('phone')
#             content = contact_form.cleaned_data.get('content')

#             # Obtén el contenido del correo desde la base de datos
#             email_content = EmailTemplate.objects.first()  # Asegúrate de tener al menos un registro en la base de datos

#             # Creamos el correo
#             email = EmailMessage(
#                 email_content.subject,
#                 email_content.message.format(name, last_name, request.user.email, phone, content),
#                 "no-contestar@inbox.mailtrap.io",
#                 [email_content.to_email],
#                 reply_to=[request.user.email],
#                 cc=[email_content.cc_email] if email_content.cc_email else None
#             )

#             try:
#                 email.send()
#                 messages.success(request, 'Su mensaje se ha enviado correctamente, en breve nos pondremos en contacto con usted.')
#                 return redirect(reverse('contact')+"?ok")
#             except Exception as e:
#                 print(traceback.format_exc())
#                 return redirect(reverse('contact')+"?fail")

#     # Obtén el usuario logueado
#     user = request.user

#     # Pasa el usuario como contexto a la plantilla
#     return render(request, "contact/contact.html",{'form':contact_form, 'user': user, 'current_page': 'contact','selected_language':get_context(request)})