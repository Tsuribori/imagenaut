from django.db import models
from imageboard.models import Board

# Create your models here.

class Rule(models.Model):
    text = models.CharField(max_length=500)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='rules', null=True, blank=True)

    def __str__(self):
        return self.text 
