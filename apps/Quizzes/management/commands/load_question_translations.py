# apps/Quizzes/management/commands/load_question_translations.py

import csv
import os
from django.core.management.base import BaseCommand
from apps.Quizzes.models import Translation


class Command(BaseCommand):
    help = 'Load question translations data from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'question_translations.csv')
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Translation.objects.create(
                    file_name=row['file_name'],
                    spanish=row['Spanish'],
                    english=row['English'],
                    score=row['Score'],
                )
        
        self.stdout.write(self.style.SUCCESS('Question translations data loaded successfully'))
