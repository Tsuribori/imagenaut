class GetIPMixin(): #Get the user IP

    def get_remote_address(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR') 
        if x_forwarded_for:
            remote_address = x_forwarded_for.split(',')[-1].strip() #If server behind proxy return the forwarded ip
        else:
            remote_address = self.request.META.get('REMOTE_ADDR') #Else return the remote_addr
        return remote_address
    
