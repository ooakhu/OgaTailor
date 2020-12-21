from django.db import models
from authentication.models import Customer
from django.utils import timezone
# Create your models here.

class Measurements(models.Model):
    id          = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    chest = models.FloatField(max_length=50, help_text='in inches')
    shoulder_width = models.FloatField(max_length=50, help_text='in inches')
    waist = models.FloatField(max_length=50, help_text='in inches')
    stomach = models.FloatField(max_length=50, help_text='in inches')
    arms_length = models.FloatField(max_length=50, help_text='in inches')
    biceps = models.FloatField(max_length=50, help_text='in inches')
    hips = models.FloatField(max_length=50, help_text='in inches')
    waist_to_ankle = models.FloatField(max_length=50, help_text='in inches')
    ankle = models.FloatField(max_length=50, help_text='in inches')
    neck = models.FloatField(max_length=50, help_text='in inches')
    thighs = models.FloatField(max_length=50, help_text='in inches')
    extra_comments = models.TextField()
    created_at      = models.DateTimeField(auto_now=False, default=timezone.now)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.email
