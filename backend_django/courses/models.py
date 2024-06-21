from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import datetime, timedelta

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Chapter(models.Model):
    chapter_title = models.CharField(max_length=255)
    next_due = models.DateTimeField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def setDue(self, days):
        self.next_due = timezone.now() + timedelta(days=days)
        self.save()

# Flashcards
class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)