import os
import tempfile
from django.template.loader import get_template
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

def generate_pdf_from_template(template_path, context_dict, output_path=None):
    try:
        template = get_template(template_path)
        html_content = template.render(context_dict)

        if output_path:
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        else:
            return HTML(string=html_content).write_pdf()

    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None

def merge_pdfs(pdf_files, output_path):
    pdf_writer = PdfWriter()

    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

def send_email(to_name, to_email, bar_fig_alternatives, pie_fig_alternatives, bar_fig_translation, pie_fig_translation, time_fig, avg_time_card_alternatives, avg_time_card_translation, results_df_alternatives, results_df_translation):
    subject = "Resultados del English Diagnostic Quiz"
    message = f'''Estimado {to_name},

Gracias por rendir el English Diagnostic Quiz. En adjunto se encuentra un archivo PDF con sus resultados.

Saludos cordiales,'''

    context = {
        'name': to_name,
        'message': message,
        'results_df_alternatives': results_df_alternatives,
        'results_df_translation': results_df_translation,
        'bar_fig_alternatives_image': os.path.abspath(bar_fig_alternatives),
        'pie_fig_alternatives_image': os.path.abspath(pie_fig_alternatives),
        'bar_fig_translation_image': os.path.abspath(bar_fig_translation),
        'pie_fig_translation_image': os.path.abspath(pie_fig_translation),
        'time_fig_image': os.path.abspath(time_fig),
        'avg_time_card_alternatives_image': os.path.abspath(avg_time_card_alternatives),
        'avg_time_card_translation_image': os.path.abspath(avg_time_card_translation)
    }

    try:
        # Generar los PDFs de las plantillas
        pdf_files = []
        for template_name in ['english_diagnostic/english_quiz_report.html', 'english_diagnostic/english_quiz_report2.html']:
            output_pdf_path = os.path.join(settings.MEDIA_ROOT, f'{template_name}.pdf')
            print(f"Generando PDF para la plantilla: {template_name}")
            pdf_path = generate_pdf_from_template(template_name, context, output_pdf_path)
            if pdf_path:
                pdf_files.append(pdf_path)
            else:
                raise Exception(f"No se pudo generar el PDF para la plantilla: {template_name}")

        # Combinar los PDFs en un solo archivo
        combined_pdf_path = os.path.join(settings.MEDIA_ROOT, 'combined_report.pdf')
        print(f"Combinando PDFs en: {combined_pdf_path}")
        merge_pdfs(pdf_files, combined_pdf_path)

        if os.path.exists(combined_pdf_path):
            print(f"Enviando correo a {to_email} con el archivo adjunto: {combined_pdf_path}")
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
            with open(combined_pdf_path, 'rb') as pdf:
                email.attach("English_Quiz_Report.pdf", pdf.read(), "application/pdf")
            email.send()

            # Eliminar las imágenes después de enviar el correo
            for image_path in [
                bar_fig_alternatives,
                pie_fig_alternatives,
                bar_fig_translation,
                pie_fig_translation,
                time_fig,
                avg_time_card_alternatives,
                avg_time_card_translation
            ]:
                if os.path.exists(image_path):
                    print(f"Eliminando imagen temporal: {image_path}")
                    os.remove(image_path)

            # Eliminar los archivos PDF combinados y temporales
            for pdf_file in pdf_files:
                if os.path.exists(pdf_file):
                    print(f"Eliminando PDF temporal: {pdf_file}")
                    os.remove(pdf_file)
            if os.path.exists(combined_pdf_path):
                print(f"Eliminando PDF combinado: {combined_pdf_path}")
                os.remove(combined_pdf_path)
        else:
            raise Exception('Hubo un error al generar el PDF.')

    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        raise

