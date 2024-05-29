# languagemiddleware.py
from django.conf import settings

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.language_data = settings.LANGUAGE_DATA

    def __call__(self, request):
        # Código a ejecutar para cada solicitud antes
        # de que la vista y más tarde el middleware sean llamados.
        request.language_data = self.language_data

        response = self.get_response(request)

        # Código a ejecutar para cada solicitud/responses después
        # de que la vista sea llamada.

        return response



