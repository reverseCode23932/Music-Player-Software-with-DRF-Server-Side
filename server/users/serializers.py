from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

class PlaylistsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Playlist
        fields = ["id", "title", "author", "songs"]

class UsersSerializer(serializers.ModelSerializer):
    joined_at = serializers.DateTimeField(read_only=True)
    is_banned = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id","username", "email", "image", "joined_at", "is_banned", "playlists"]
    
class SongsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    song = serializers.FileField(write_only=True)
    song_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Song
        fields = ["id", "title", "song", "song_url", "image", "author", "created_at"]

    def get_song_url(self, obj):
        if obj.song:
            return obj.song.url
        return None
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if getattr(self.user, "is_banned", False):
            raise serializers.ValidationError(f"{self.user.username} account is banned.") #type:ignore

        return data