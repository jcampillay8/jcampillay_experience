# Generated by Django 4.2.9 on 2024-06-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Quizzes", "0002_alter_quiz_imagen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="description",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="quiz", name="title", field=models.CharField(max_length=255),
        ),
    ]
