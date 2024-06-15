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
from django.urls import reverse

@login_required(login_url='login')
def contact_home(request):
    return render(request, 'contact/contact_home.html',{'current_pages':'contact_home'})