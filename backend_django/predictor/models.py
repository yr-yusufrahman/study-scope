from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from courses.models import Course, Chapter

# Create your models here.

class Revision(models.Model):
    # Manual inputs
    mistakes = models.IntegerField()
    inputs = models.IntegerField()
    number_of_reveals = models.IntegerField(default=0) # Number of reveal questions

    date = models.DateTimeField(auto_now_add=True)
    days_since = models.IntegerField(default=0) # Days since last revision
    mistake_rate = models.FloatField(default=0) # Change in mistake score since last revision
    is_loss = models.BooleanField(default=False) # True if there was a drop off

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


    # Override save method to calculate other field values
    def save(self, *args, **kwargs):
        # Get the most recent revision for the same chapter
        last_revision = Revision.objects.filter(chapter=self.chapter).order_by('-date').first()
        
        # Find the days since the last revision and if there was a drop off
        if last_revision:
            # Calculate the difference in days between now and the last revision date
            delta = datetime.now().date() - last_revision.date.date()
            self.days_since = delta.days

            # Check if there was a drop off
            # 
            # Define a drop off as:
            # Mistake score = mistakes / inputs * 100
            # If mistakes score increased by 25% = small drop off
            # If mistakes score increased by 40% = large drop off

            # For now, we'll just use 20% as the threshold
            last_mistake_score = (last_revision.mistakes / last_revision.inputs) * 100
            last_mistake_score = round(last_mistake_score, 4)

            current_mistake_score = (self.mistakes / self.inputs) * 100
            current_mistake_score = round(current_mistake_score, 4)

            # Calculate the change in mistake score
            self.mistake_rate = current_mistake_score - last_mistake_score

            # If mistake rate increased by 25%, there was a drop off
            if self.mistake_rate >= 25:
                self.is_loss = True
            else:
                self.is_loss = False


        super().save(*args, **kwargs)


# Model for storing predictor parameters. Two for each course? To handle drop-offs and non-drop-offs.
class Predictor(models.Model):
    parameters = models.JSONField()
    drop_off = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

