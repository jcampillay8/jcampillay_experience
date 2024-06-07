# utils.py
def get_context(request):
    # Obtener los datos del idioma de la solicitud
    language_data = request.language_data

    # Determinar el idioma seleccionado por el usuario
    selected_language = request.session.get('language', 'English')

    # Obtener todos los datos del idioma seleccionado
    selected_language_data = language_data[selected_language]

    context = {
        'selected_language': selected_language_data,
        'fieldValues': request.POST,
    }

    return context
