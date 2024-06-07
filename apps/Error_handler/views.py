from django.shortcuts import render
from django.views.generic import (View, TemplateView)

# Create your views here.

class Error404View(TemplateView):
    template_name = 'ErrorHandler/error_404.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request, exception=None):
            r = v(request)
            r.render()
            return r
        return view

class Error505View(TemplateView):
    template_name = 'ErrorHandler/error_505.html'

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r
        return view