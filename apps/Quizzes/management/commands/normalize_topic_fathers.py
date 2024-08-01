# apps/content_management/management/commands/normalize_topic_fathers.py

from django.core.management.base import BaseCommand
from apps.content_management.models import ListTopicFather

class Command(BaseCommand):
    help = 'Normalize topic_father names in ListTopicFather'

    def handle(self, *args, **kwargs):
        for topic_father in ListTopicFather.objects.all():
            normalized_name = topic_father.topic_father.strip().lower()
            if topic_father.topic_father != normalized_name:
                topic_father.topic_father = normalized_name
                topic_father.save()
                self.stdout.write(self.style.SUCCESS(f'Normalized: {normalized_name}'))
        self.stdout.write(self.style.SUCCESS('All topic_father names have been normalized'))
