from django.db import models
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.core.signing import Signer
from sorl.thumbnail import ImageField
from embed_video.fields import EmbedVideoField
#from django.utils.functional import cached_property

# Create your models here.

class DateMixin(): #Format the date in templates for thread and post
    def get_date(self):
        return self.time_made.strftime("%a %H:%M, %d %b %Y")


class Board(models.Model):
    name = models.CharField(max_length=31, unique=True)
    description = models.CharField(max_length=300, null=True)
    slug = models.SlugField(max_length=31, unique=True)
    def get_absolute_url(self):
        return reverse('imageboard_thread_list', kwargs={'board': self.slug})
    def get_thread_create_url(self):
        return reverse('imageboard_thread_create', kwargs={'board': self.slug})
    def get_catalog_url(self):
        return reverse('imageboard_thread_catalog', kwargs={'board': self.slug})
    def get_reported_threads_url(self):
        return '{}?board={}'.format(reverse('dj-mod:moderation_thread_report_list'), self.slug)
    def get_reported_posts_url(self):
        return '{}?board={}'.format(reverse('dj-mod:moderation_userpost_report_list'), self.slug)
    def get_archive_url(self):
        return reverse('archive_thread_list', kwargs={'board': self.slug}) 
    def __str__(self):
        return self.name

class Thread(models.Model, DateMixin):
    def get_thread_number():
        max_number = Thread.objects.all().aggregate(models.Max('thread_number'))['thread_number__max']
        if max_number == None:
            return 0
        else:
            return max_number + 1

    thread_number = models.PositiveIntegerField(unique=True, default=get_thread_number, editable=False)
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=20, default='Anonymous')
    time_made = models.DateTimeField(default=timezone.now, editable=False)
    post = models.CharField(max_length=5000, blank=False)
    bumb_order = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='threads')
    ip_address = models.GenericIPAddressField()
    archived = models.BooleanField(default=False)
    bumb_limit_reached = models.BooleanField(default=False) 
    reported = models.BooleanField(default=False)
    image = ImageField(upload_to='images/', blank=False)
    pinned = models.BooleanField(default=False)
    embed = EmbedVideoField(blank=True, null=True, help_text='Youtube, Vimeo or Soundcloud URL')
    id_enabled = models.BooleanField(default=False, verbose_name='Enable poster IDs')
    poster_id = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(str(self.thread_number), self.subject)

    def get_absolute_url(self):
        return reverse('imageboard_thread_page', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
    def get_post_create_url(self):
        return reverse('imageboard_userpost_create', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
    def get_delete_url(self):
        return reverse('imageboard_thread_delete', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
    def get_ban_url(self):
        return reverse('dj-mod:moderation_thread_ban', kwargs={'thread_number': self.thread_number})
    def get_report_url(self):
        return reverse('imageboard_thread_report', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
    def get_report_dismiss_url(self):
        return reverse('dj-mod:moderation_thread_report_dismiss', kwargs={'thread_number': self.thread_number})
    def get_archive_url(self):
        return reverse('archive_thread_list', kwargs={'board': self.board.slug})
    def get_archive_year_url(self):
        return reverse('archive_thread_year_list', kwargs={'board': self.board.slug, 'year': self.time_made.year})
    def get_archive_month_url(self):
        return reverse('archive_thread_month_list', kwargs={'board': self.board.slug, 'year': self.time_made.year, 'month': self.time_made.month})
    def get_archive_day_url(self):
        return reverse(
            'archive_thread_day_list', kwargs={'board': self.board.slug, 'year': self.time_made.year, 'month': self.time_made.month, 'day': self.time_made.day})

    def generate_poster_id(self):
        value = str(self.ip_address) + str(self.thread_number)
        signer = Signer()
        unique_id = signer.sign(value)[-10:] #Get the last ten chars of the hash
        return unique_id

 
    def save(self, *args, **kwargs):
        active_threads = Thread.objects.filter(board=self.board, archived=False).count()
        if active_threads >= 100 and self.archived==False: #Prevent recursion by checking self.archived==False 
            last_thread = Thread.objects.filter(board=self.board, archived=False).earliest('bumb_order') #Get the last thread i.e. the one with the lowest bumb_order
            last_thread.archived = True #Archive it
            last_thread.save()
        if self.id_enabled:
            self.poster_id = self.generate_poster_id()
        super(Thread, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-pinned', '-bumb_order']
        indexes = [
            models.Index(fields=['thread_number']),
        ]

class UserPost(models.Model, DateMixin):
    def get_post_number():
        max_number = UserPost.objects.all().aggregate(models.Max('post_number'))['post_number__max']
        if max_number == None:
            return 0
        else:
            return max_number + 1
    post_number = models.PositiveIntegerField(unique=True, default=get_post_number)
    name = models.CharField(max_length=20, default='Anonymous')
    time_made = models.DateTimeField(auto_now=True)
    post = models.CharField(max_length=5000, blank=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    ip_address = models.GenericIPAddressField()
    sage = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    image = ImageField(upload_to='images/', blank=True, null=True)
    embed = EmbedVideoField(blank=True, null=True, help_text='Youtube, Vimeo or Soundcloud URL')
    poster_id = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.post_number)

    def get_absolute_url(self): #No individual view for post, so just return the threads page 
        return self.thread.get_absolute_url()
    def get_delete_url(self):
        return reverse('imageboard_userpost_delete', kwargs={
            'board': self.thread.board.slug, 'thread_number': self.thread.thread_number, 'post_number': self.post_number})
    def get_ban_url(self):
        return reverse('dj-mod:moderation_userpost_ban', kwargs={'post_number': self.post_number})
    def get_report_url(self):
        return reverse('imageboard_userpost_report', kwargs={
            'board': self.thread.board.slug, 'thread_number': self.thread.thread_number, 'post_number': self.post_number})
    def get_report_dismiss_url(self):
        return reverse('dj-mod:moderation_userpost_report_dismiss', kwargs={'post_number': self.post_number})


    def generate_poster_id(self): #Generate a poster id for a thread based on the posters IP and the threads number. 
        value = str(self.ip_address) + str(self.thread.thread_number)
        signer = Signer()
        unique_id = signer.sign(value)[-10:] #Get the last ten chars of the hash
        return unique_id
    
    def save(self, *args, **kwargs):
        if self.sage==False and self.thread.bumb_limit_reached==False:
            self.thread.bumb_order=timezone.now()
        post_count = self.thread.posts.count() 
        if post_count >= 499 and self.thread.pinned == False:
            self.thread.archived = True
        elif post_count >= 349:
            self.thread.bumb_limit_reached = True
        if self.thread.id_enabled: 
            self.poster_id = self.generate_poster_id()
        self.thread.save()
        super(UserPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ['post_number']

