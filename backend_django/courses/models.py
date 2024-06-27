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
    order = models.IntegerField(default=-1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def setDue(self, days):
        self.next_due = timezone.now() + timedelta(days=days)
        self.save()

    def switchCourse(self):
        last_index = Chapter.objects.filter(course=self.course).count()-1
        self.order = last_index

        # Remove any spaces in the title
        title = self.chapter_title.replace(" ", "")
        
        # Check if the new course has a chapter with the same title
        exists = Chapter.objects.filter(course=self.course, chapter_title=title).first()
        if exists:
            copy = 1
            while exists:
                copy_title = f"{title} ({str(copy)})"
                exists = Chapter.objects.filter(course=self.course, chapter_title=copy_title).first()
                if exists:
                    copy += 1
            self.chapter_title = copy_title
            self.save()
        else:
            self.save()


# Flashcards
class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)