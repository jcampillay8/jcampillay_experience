# apps/content_management/management/commands/load_list_topic_father.py

import csv
import os
from django.core.management.base import BaseCommand
from apps.content_management.models import ListTopicFather

class Command(BaseCommand):
    help = 'Load list topic father from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'list_topic_father.csv')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return
        
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ListTopicFather.objects.create(
                    id=row['ID'],
                    topic_father=row[' Topic_Father'],
                )
        
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
