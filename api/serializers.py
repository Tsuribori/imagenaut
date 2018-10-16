from imageboard.models import Board, Thread
from rest_framework import serializers

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_board-detail', lookup_field='slug')
    threads = serializers.HyperlinkedRelatedField(many=True, view_name='api_thread-detail', lookup_field='thread_number', read_only=True)

    class Meta:
        model = Board
        fields = ('url', 'name', 'description', 'slug', 'threads')

class ThreadSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_thread-detail', lookup_field='thread_number')
    board = serializers.HyperlinkedRelatedField(view_name='api_board-detail', lookup_field='slug', queryset=Board.objects.all())

    class Meta:
        model = Thread
        fields = ('thread_number', 'url', 'subject', 'name', 'time_made', 'post', 'board', 'id_enabled', 'poster_id', 'pinned', 'embed', 'image', 'bumb_limit_reached', 'archived',)
        read_only_fields = ('archived',)


