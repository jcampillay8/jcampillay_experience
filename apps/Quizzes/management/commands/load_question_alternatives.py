# apps/Quizzes/management/commands/load_question_alternatives.py

import csv
import os
from django.core.management.base import BaseCommand
from apps.Quizzes.models import StructuredEnglishGrammarCourse


class Command(BaseCommand):
    help = 'Load question alternatives data from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'question_alternatives.csv')
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StructuredEnglishGrammarCourse.objects.create(
                    file_name=row['file_name'],
                    question=row['question'],
                    options=row['options'],
                    answer=row['answer'],
                    explanation=row['explanation'],
                    value=row['value'],
                )
        
        self.stdout.write(self.style.SUCCESS('Question alternatives data loaded successfully'))
