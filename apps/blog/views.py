from django import forms
import django
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.translation import gettext as _



# Create your views here.
@login_required(login_url='login')
def blog_home(request):
    return render(request, 'blog/blog_home.html', {'current_pages': ['blog_home', 'about_me_home']})
