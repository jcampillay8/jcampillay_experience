from django import forms
import django
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render
from .models import Quiz
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# from apps.Quizzes.models import Post, UserQuestionValue, Question
from apps.Quizzes.forms import QuizForm
# from apps.Quizzes.gcp_trainer_app import app
from django.utils.translation import gettext as _



def quiz_index(request):
    return redirect('quiz_post')

@login_required(login_url='login')
def createQuiz(request):

    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)    
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author_id = request.user.id  # Asegúrate de que 'author_id' coincide con el nombre del campo en tu modelo
            quiz.save()
            print('hola')
            return redirect('quiz_post')
    else:

        form = QuizForm()
        return render(request, 'Quizzes/quiz_creation.html', {'form': form, 'author_id': request.user.id})


@login_required(login_url='login')
def seeQuiz(request, pk=None):
    if pk is not None:
        quiz = get_object_or_404(Post, id=pk)
        tieneLike = request.user in quiz.likes.all()
    else:
        quiz = None
        tieneLike = False

    quizzes = Quiz.objects.all()
    paginator = Paginator(quizzes, 3)
    num_pagina = request.GET.get('page')
    pagina_actual = paginator.get_page(num_pagina)

    context = {
        'quiz':quiz, 
        'likes': quiz.cantidad_likes() if quiz else 0, 
        'tiene_like': tieneLike,
        'current_page': 'Quizzes',
        'quizzes': pagina_actual
    }

    return render(request, 'Quizzes/quiz_index.html', context)


@login_required(login_url='login')
def deleteQuiz(request, pk):
    # post = Post.objects.get(id=pk)
    quiz = get_object_or_404(Quiz, id=pk)
    if quiz.author == request.user:
        if request.method == 'POST':
            quiz.delete()
            return redirect('index')

            context = {
                'quiz':quiz
                }
        
        return render(request, 'Quizzes/quiz_delete.html', context)
    else:
        return redirect(f'/quiz/{quiz.id}')