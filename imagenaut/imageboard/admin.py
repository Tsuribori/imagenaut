from django.contrib import admin
from .models import Board, Thread, UserPost
# Register your models here.
admin.site.register(Board)
admin.site.register(Thread)
admin.site.register(UserPost)

