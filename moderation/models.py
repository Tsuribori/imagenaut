from django.db import models

# Create your models here.

class Transgression(models.Model):
    ip_address = models.GenericIPAddressField()
    banned_until = models.DateTimeField()
    reason = models.CharField(max_length=150)
    
    def __str__(self):
        return "{}: {}".format(self.ip_address, self.banned_until)
     
