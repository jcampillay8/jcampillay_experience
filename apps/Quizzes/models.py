# models.py
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.csrf import csrf_exempt

class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to='core/assets/images/quizzes/', default='imagen')
    likes = models.ManyToManyField(User, related_name='post_likes')

    def cantidad_likes(self):
        return self.likes.count()


class StructuredEnglishGrammarCourse(models.Model):
    file_name = models.CharField(max_length=255)
    question = models.TextField()
    options = models.JSONField()
    answer = models.IntegerField()
    explanation = models.TextField()
    value = models.IntegerField()

    def __str__(self):
        return self.question

class Translation(models.Model):
    file_name = models.CharField(max_length=255)
    spanish = models.TextField()
    english = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return self.spanish
