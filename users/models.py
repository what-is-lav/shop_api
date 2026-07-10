from django.db import models
from django.contrib.auth.models import User


class Verifications(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirm_code')
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.code
    

# Create your models here.
