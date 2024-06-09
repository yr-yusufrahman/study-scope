from django.db import models
import datetime
from django.contrib.auth.models import User
from courses.models import Course, Chapter

# Create your models here.

class Revision(models.Model):
    mistakes = models.IntegerField()
    inputs = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_loss = models.BooleanField() # True if there was a drop off
    days_since = models.IntegerField() # Days since last revision
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Get the most recent revision for the same chapter
        last_revision = Revision.objects.filter(chapter=self.chapter).order_by('-date').first()
        
        if last_revision:
            # Calculate the difference in days between now and the last revision date
            delta = datetime.now().date() - last_revision.date.date()
            self.days_since = delta.days
        else:
            # If there's no previous revision, set days_since to 0
            self.days_since = 0

        super().save(*args, **kwargs)


# Model for storing predictor parameters. Two for each course? To handle drop-offs and non-drop-offs.
class Predictor(models.Model):
    parameters = models.JSONField()
    drop_off = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

