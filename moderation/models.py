from django.db import models
from imageboard.models import Board

# Create your models here.

class Transgression(models.Model):
    ip_address = models.GenericIPAddressField()
    banned_until = models.DateTimeField()
    reason = models.CharField(max_length=150)
    global_ban = models.BooleanField(default=False)
    banned_from = models.ForeignKey(Board, on_delete=models.CASCADE, null=True) 
 
    def __str__(self):
        return "{}: {}".format(self.ip_address, self.banned_until)
    
 
