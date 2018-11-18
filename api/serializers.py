from imageboard.utils import GetIPMixin, BanMixin, CooldownMixin
from imageboard.models import Board, Thread, UserPost
from django.urls import resolve
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_validator.fields import RestCaptchaField

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_board-detail', lookup_field='slug')
    threads = serializers.HyperlinkedRelatedField(many=True, view_name='api_thread-detail', lookup_field='thread_number', read_only=True)
    thread_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BoardSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')
        if context: 
            request = context['request']
            if request.path == reverse('api_board-list'):
                self.fields.pop('threads')


    def get_thread_count(self, obj):
        return obj.threads.count()

    class Meta:
        model = Board
        fields = ('url', 'name', 'description', 'slug', 'thread_count', 'threads')

class ThreadSerializer(serializers.ModelSerializer, GetIPMixin, BanMixin, CooldownMixin):
    url = serializers.HyperlinkedIdentityField(view_name='api_thread-detail', lookup_field='thread_number')
    board = serializers.HyperlinkedRelatedField(view_name='api_board-detail', lookup_field='slug', queryset=Board.objects.all())
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='api_post-detail', lookup_field='post_number', read_only=True)
    post_count = serializers.SerializerMethodField()
    captcha_key = RestCaptchaField(write_only=True)

    def __init__(self, *args, **kwargs): #Exclude the 'posts' field if the view is api_thread-list to prevent a massive request
        super(ThreadSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context['request']
            self.ip_address = self.get_remote_address()
            if self.request.path == reverse('api_thread-list'):
                self.fields.pop('posts')

    def create(self, validated_data):
        validated_data.pop('captcha_key')
        validated_data['ip_address'] = self.ip_address
        if self.request.method == 'POST':
            board = validated_data['board']
            if self.user_is_banned(board):
                raise ValidationError("You're banned from this board.")
            if self.user_on_cooldown(Thread):
                raise ValidationError("You need to wait longer before making a new thread.")
            
        instance = super().create(validated_data)
        return instance

    def get_post_count(self, obj):
        return obj.posts.count()
    
    class Meta:
        model = Thread
        fields = ('thread_number', 'url', 'subject', 'name', 'time_made', 'post', 'board', 'id_enabled', 'poster_id', 'pinned', 'embed', 'image', 'bumb_limit_reached', 'archived', 'post_count', 'posts', 'captcha_key')
        read_only_fields = ('archived', 'pinned', 'bumb_limit_reached')

class UserPostSerializer(serializers.ModelSerializer, GetIPMixin, BanMixin, CooldownMixin):
    url = serializers.HyperlinkedIdentityField(view_name='api_post-detail', lookup_field='post_number')
    thread = serializers.HyperlinkedRelatedField(view_name='api_thread-detail', lookup_field='thread_number', queryset=Thread.objects.all())
    captcha_key = RestCaptchaField(write_only=True)

    def __init__(self, *args, **kwargs): 
        super(UserPostSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')
        if context:
            self.request = context['request']
            self.ip_address = self.get_remote_address()
            
    def create(self, validated_data):
        validated_data.pop('captcha_key')
        validated_data['ip_address'] = self.ip_address
        if self.request.method == 'POST':
            board = validated_data['thread'].board
            if self.user_is_banned(board):
                raise ValidationError("You're banned from this board.")
            if self.user_on_cooldown(UserPost):
                raise ValidationError("You need to wait longer before making a new post.")
            
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = UserPost
        fields = ('post_number', 'url', 'name', 'time_made', 'post', 'thread', 'sage', 'image', 'embed', 'poster_id', 'captcha_key') 
