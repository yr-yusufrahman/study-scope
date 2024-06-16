from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Chapter

from datetime import datetime
from predictor.helpers.loadModel import defaultModelParams, defaultTree
import joblib, io, os, numpy as np

# Create your models here.

class Revision(models.Model):
    mistakes = models.IntegerField()
    inputs = models.IntegerField()
    percentage_of_reveals = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    # Calculated by looking at the previous and next revision session
    days_since = models.IntegerField(default=-1) # calculated in save method
    interval = models.IntegerField(default=-1) # Days until next revision session
    mistake_rate = models.FloatField(default=-1) # Change in mistake score from now to the next revision session
    is_loss = models.BooleanField(default=False) # True if there was a drop off

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


    # Create method to calculate other field values
    def complete(self, *args, **kwargs):
        # Get the most recent revision for the same chapter
        last_revision = Revision.objects.filter(chapter=self.chapter).exclude(id=self.pk).order_by('-date').first()
        
        # Check if the chapter was revised before
        if last_revision:
            # Interval: Get the days since the last revision
            #delta = self.date.date() - last_revision.date.date()
            last_interval = self.days_since #delta.days

            # Check if there was a drop off since the last revision
            # If mistakes score increased by 25% = small drop off
            # If mistakes score increased by 40% = large drop off
            last_mistake_score = (last_revision.mistakes / last_revision.inputs) * 100
            last_mistake_score = round(last_mistake_score, 4)

            current_mistake_score = (self.mistakes / self.inputs) * 100
            current_mistake_score = round(current_mistake_score, 4)

            # Mistake score: Calculate the change in mistake score
            change = current_mistake_score - last_mistake_score
            
            # Is loss: If mistake rate increased by 25%, there was a drop off so shorten the interval by 20%
            loss = False
            if change >= 25:
                loss = True
                last_interval = int(last_interval * 0.8)

            # Complete the last revision session values
            last_revision.interval = last_interval # If there was no drop off, interval of last revision = days_since for this
            last_revision.mistake_rate = change
            last_revision.is_loss = loss
            last_revision.save() # this causes error as it will use the modified save method which will cause an infinite loop 


    def setDaysSince(self):
        last_revision = Revision.objects.filter(chapter=self.chapter).exclude(id=self.pk).order_by('-date').first()
        if last_revision:
            # Set the days since the last revision
            delta = self.date.date() - last_revision.date.date()
            days_since = delta.days
            self.days_since = days_since
            self.save()
                  


# mistake score, inputs, number of reveals
# Session 0: 0.3, 14, 3 

# 6 days later

# Session 1: 0.9, 11, 5
#
# 10 days later
#
# Session 2: 1.5, 10, 8 

# This is a drop off because the mistake score increased by 25%
# What should be saved as a data point?

# X values: 0.9, 11, 5 
# Y value: 7 days 
# 10 days - decrease by 25% (Depending on how much the mistake score increased by, reduce days by a certain percentage)

# This means the next time the user revises a chapter and gets values similar to: 0.9, 11, 5
# The model should predict that the next revision should be in 7 days
# The model is trying to prevent memory decay in the least expensive way possible - so no need to revise every day 




# Model for storing predictor parameters. Two for each course? To handle drop-offs and non-drop-offs.
class Predictor(models.Model):
    #parameters = models.JSONField(default=dict, null=True, blank=True)
    drop_off = models.BooleanField()
    tree = models.BinaryField(default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Save the parameters
            #params = defaultModelParams()
            #self.parameters = params
            self.drop_off = True
            self.tree = defaultTree()
        super().save(*args, **kwargs)
