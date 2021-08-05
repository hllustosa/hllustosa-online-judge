from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    TEACHER = 'T'
    STUDENT = 'S'
    
    USER_OPTIONS = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=USER_OPTIONS)