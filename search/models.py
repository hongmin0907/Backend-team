from django.db import models
from stay.models import Stay
# Create your models here.


class Search(models.Model):
    searchKey = models.CharField(max_length=50, unique=True)
    stays = models.ManyToManyField(Stay, related_name='searchstays', blank=True)