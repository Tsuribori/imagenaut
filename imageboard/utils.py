from moderation.models import Transgression
from django.utils import timezone

class GetIPMixin(): #Get the user IP

    def get_remote_address(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR') 
        if x_forwarded_for:
            remote_address = x_forwarded_for.split(',')[-1].strip() #If server behind proxy return the forwarded ip
        else:
            remote_address = self.request.META.get('REMOTE_ADDR') #Else return the remote_addr
        return remote_address
   


class BanMixin():

    def user_is_banned(self): #Return true if ban found for ip, false if not found
        ip_addr = self.get_remote_address()
        bans = Transgression.objects.filter(ip_address__iexact=ip_addr)
        for ban in bans:
            if ban.banned_until < timezone.now():  #Delete bans that have expired
                ban.delete() 
        return bans.exists()
         
