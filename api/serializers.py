from imageboard.models import Board, Thread, UserPost
from rest_framework import serializers
from rest_framework.reverse import reverse

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_board-detail', lookup_field='slug')
    threads = serializers.HyperlinkedRelatedField(many=True, view_name='api_thread-detail', lookup_field='thread_number', read_only=True)
    thread_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BoardSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')
        many = False
        if context: 
            request = context['request']
            if request.path == reverse('api_board-list'):
                self.fields.pop('threads')

    def get_thread_count(self, obj):
        return obj.threads.count()

    class Meta:
        model = Board
        fields = ('url', 'name', 'description', 'slug', 'thread_count', 'threads')

class ThreadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_thread-detail', lookup_field='thread_number')
    board = serializers.HyperlinkedRelatedField(view_name='api_board-detail', lookup_field='slug', queryset=Board.objects.all())
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='api_post-detail', lookup_field='post_number', read_only=True)
    post_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs): #Exclude the 'posts' field if the view is api_thread-list to prevent a massive request
        super(ThreadSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context')
        if context:
            request = context['request']
            if request.path == reverse('api_thread-list'):
                self.fields.pop('posts')

    def get_post_count(self, obj):
        return obj.posts.count()
    
    class Meta:
        model = Thread
        fields = ('thread_number', 'url', 'subject', 'name', 'time_made', 'post', 'board', 'id_enabled', 'poster_id', 'pinned', 'embed', 'image', 'bumb_limit_reached', 'archived', 'post_count', 'posts')
        read_only_fields = ('archived', 'pinned', 'bumb_limit_reached')

class UserPostSerializer(serializers.ModelSerializer, RestCaptchaSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_post-detail', lookup_field='post_number')
    thread = serializers.HyperlinkedRelatedField(view_name='api_thread-detail', lookup_field='thread_number', queryset=Thread.objects.all())

    class Meta:
        model = UserPost
        fields = ('post_number', 'url', 'name', 'time_made', 'post', 'thread', 'sage', 'image', 'embed', 'poster_id') 
