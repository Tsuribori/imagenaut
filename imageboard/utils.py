import re
from django.conf import settings 
from django.core.signing import Signer
from .models import Thread, UserPost
from moderation.models import Transgression
from imageboard.models import Board
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

    def user_is_banned(self, board): #Return true if ban found for ip, false if not found
        try:
            if self.request:
                ip_addr = self.get_remote_address()
                bans = Transgression.objects.filter(ip_address__iexact=ip_addr)
                ban_list = []
                for ban in bans:
                    if ban.banned_until < timezone.now():  #Delete bans that have expired
                        ban.delete()
                    elif ban.global_ban == True or ban.banned_from == board: #
                        ban_list.append(ban.banned_until)
                return len(ban_list) > 0
        
        except AttributeError:
            return None
        

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
       

class MakeTripcode():

    def create_tripcode(self, string):
        match = re.search('#[\d\w\s]+', string)
        if match: 
            password = match.group(0)
            signer = Signer()
            tripcode = '!{}'.format(signer.sign(password)[-10:])
            string = string.replace(password, tripcode)
        return string
