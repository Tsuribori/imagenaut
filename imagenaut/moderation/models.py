from django.db import models
from imageboard.models import Board

# Create your models here.

class Transgression(models.Model):
    ip_address = models.GenericIPAddressField()
    banned_until = models.DateTimeField(help_text='Format: YYYY-MM-DD hh:mm. Eg. 2049-12-24 18:05')
    reason = models.CharField(max_length=150)
    global_ban = models.BooleanField(default=False)
    banned_from = models.ForeignKey(Board, on_delete=models.CASCADE, null=True) 
 
    def __str__(self):
        return "{}: {}".format(self.ip_address, self.banned_until)
    
 
