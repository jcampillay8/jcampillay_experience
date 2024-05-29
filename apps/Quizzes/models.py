# models.py
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.csrf import csrf_exempt

class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=None)
    description = models.CharField(max_length=None)
    imagen = models.ImageField(upload_to='core/assets/images/quizzes/', default='imagen')
    likes = models.ManyToManyField(User, related_name='post_likes')

    def cantidad_likes(self):
        return self.likes.count()

        