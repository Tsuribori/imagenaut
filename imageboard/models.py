from django.db import models
# Create your models here.

class Thread(models.Model):
    def get_thread_number():
        max_number = Thread.objects.all().aggregate(models.Max('thread_number'))['thread_number__max']
        if max_number == None:
            return 0
        else:
            return max_number + 1

    thread_number = models.PositiveIntegerField(unique=True, default=get_thread_number)
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=20, default='Anonymous')
    time_made = models.DateTimeField(auto_now=True)
    post = models.CharField(max_length=5000, blank=False)
    bumb_order = models.PositiveIntegerField(default=0)
    def __str__(self):
        return "{} {}".format(str(self.thread_number), self.subject)
    class Meta:
        ordering = ['-bumb_order']

class UserPost(models.Model):
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

    def save(self, *args, **kwargs):
        self.thread.bumb_order=self.post_number
        self.thread.save()
        super(UserPost, self).save(*args, **kwargs)
    class Meta:
        ordering = ['-post_number']
