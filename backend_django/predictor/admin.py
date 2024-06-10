from django.contrib import admin

# Register your models here.
from .models import Revision, Predictor

admin.site.register(Revision)
admin.site.register(Predictor)