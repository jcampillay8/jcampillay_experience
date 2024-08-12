import os
import tempfile
from django.template.loader import get_template
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.conf import settings
from PyPDF2 import PdfReader, PdfWriter

def generate_pdf_from_template(template_paths, context_dict):
    pdf_files = []
    for template_path in template_paths:
        try:
            template = get_template(template_path)
            html_content = template.render(context_dict)
            if not isinstance(html_content, str):
                raise ValueError("El contenido HTML no es un string válido.")
            pdf_file = HTML(string=html_content).write_pdf()
            pdf_files.append(pdf_file)
        except Exception as e:
            print(f"Error al generar el PDF para la plantilla: {template_path}")
            print(f"Error: {str(e)}")
            raise
    return pdf_files

def merge_pdfs(pdf_files, output_path):
    pdf_writer = PdfWriter()

    for pdf_bytes in pdf_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file_path = tmp_file.name

        pdf_reader = PdfReader(tmp_file_path)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        
        os.remove(tmp_file_path)

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
        pdf_files = generate_pdf_from_template(
            ['english_diagnostic/english_quiz_report.html', 'english_diagnostic/english_quiz_report2.html'],
            context
        )
        combined_pdf_path = "combined_report.pdf"
        merge_pdfs(pdf_files, combined_pdf_path)

        if os.path.exists(combined_pdf_path):
            # Asegurarte de que EmailMessage esté correctamente importado y utilizado
            email = EmailMessage(
                subject=subject, 
                body=message, 
                from_email=settings.DEFAULT_FROM_EMAIL, 
                to=[to_email]
            )
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
                    os.remove(image_path)

            # Eliminar el archivo PDF combinado
            if os.path.exists(combined_pdf_path):
                os.remove(combined_pdf_path)
        else:
            raise Exception('Hubo un error al generar el PDF.')

    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        raise
