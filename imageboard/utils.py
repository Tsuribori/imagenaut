from django.conf import settings 
from .models import Thread, UserPost
from moderation.models import Transgression
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

class GetIPMixin(): #Get the user IP

    def get_remote_address(self):
        try: 
            if self.request:
                x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR') 
                if x_forwarded_for:
                    remote_address = x_forwarded_for.split(',')[-1].strip() #If server behind proxy return the forwarded ip
                else:
                    remote_address = self.request.META.get('REMOTE_ADDR') #Else return the remote_addr
                return remote_address
        
        except AttributeError:
            return None
   


class BanMixin():

    def user_is_banned(self): #Return true if ban found for ip, false if not found
        ip_addr = self.get_remote_address()
        bans = Transgression.objects.filter(ip_address__iexact=ip_addr)
        ban_list = []
        for ban in bans:
            if ban.banned_until < timezone.now():  #Delete bans that have expired
                ban.delete()
            else:
                ban_list.append(ban.banned_until)
        return len(ban_list) > 0
        

class CooldownMixin():
    def user_on_cooldown(self, model):
        ip_addr = self.get_remote_address()
        try:
            post = model.objects.filter(ip_address__iexact=ip_addr).latest('time_made')
        except ObjectDoesNotExist:
            return False
        if post:
            if model == Thread:
                cooldown = settings.THREAD_COOLDOWN
            elif model == UserPost:
                cooldown = settings.POST_COOLDOWN
            if timezone.now() - post.time_made < timedelta(seconds=cooldown):
                return True
        return False
        
