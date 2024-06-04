from django.utils.translation import get_language

def language_code(request):
    return {
        'LANGUAGE_CODE': get_language(),
    }
