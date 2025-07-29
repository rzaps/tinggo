from django.utils import translation
from django.conf import settings

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if language is specified in query parameters
        lang_code = request.GET.get('lang')
        if lang_code and lang_code in [lang[0] for lang in settings.LANGUAGES]:
            # Set language for this request
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
        else:
            # Use default language
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE

        response = self.get_response(request)
        return response 