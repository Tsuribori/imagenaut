from django.db import models
from django.urls import reverse
from datetime import datetime
# Create your models here.

class DateMixin(): #Format the date in templates for thread and post
    def get_date(self):
        return self.time_made.strftime("%a %H:%M, %d %b %Y")


class Board(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True)
    def get_thread_create_url(self):
        return reverse('imageboard_thread_create', kwargs={'board': self.slug})

    def __str__(self):
        return self.name

class Thread(models.Model, DateMixin):
    def get_thread_number():
        max_number = Thread.objects.all().aggregate(models.Max('thread_number'))['thread_number__max']
        if max_number == None:
            return 0
        else:
            return max_number + 1

    thread_number = models.PositiveIntegerField(unique=True, default=get_thread_number)
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=20, default='Anonymous')
    time_made = models.DateTimeField(auto_now_add=True)
    post = models.CharField(max_length=5000, blank=False)
    bumb_order = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    def __str__(self):
        return "{} {}".format(str(self.thread_number), self.subject)
    def get_absolute_url(self):
        return reverse('imageboard_thread_page', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
    def get_post_create_url(self):
        return reverse('imageboard_userpost_create', kwargs={'board': self.board.slug, 'thread_number': self.thread_number})
        
    class Meta:
        ordering = ['-bumb_order']

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
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post_number)

    def get_absolute_url(self): #No individual view for post, so just return the threads page 
        return self.thread.get_absolute_url()
    def save(self, *args, **kwargs):
        self.thread.bumb_order=self.time_made
        self.thread.save()
        super(UserPost, self).save(*args, **kwargs)
    class Meta:
        ordering = ['post_number']

