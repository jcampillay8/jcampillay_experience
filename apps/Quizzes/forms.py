from django import forms
from apps.Quizzes.models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'imagen')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
