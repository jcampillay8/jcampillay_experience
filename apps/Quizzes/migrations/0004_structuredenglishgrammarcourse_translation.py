# Generated by Django 4.2.9 on 2024-07-29 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizzes', '0003_alter_quiz_description_alter_quiz_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructuredEnglishGrammarCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('question', models.TextField()),
                ('options', models.JSONField()),
                ('answer', models.IntegerField()),
                ('explanation', models.TextField()),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('spanish', models.TextField()),
                ('english', models.TextField()),
                ('score', models.IntegerField()),
            ],
        ),
    ]
