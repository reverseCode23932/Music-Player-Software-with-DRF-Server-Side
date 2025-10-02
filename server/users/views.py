from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
import os

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistsSerializer
    lookup_field = "name"
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist = serializer.save(owner=self.request.user)
        return Response({
            "message": "Playlist created successfully",
            "playlist": PlaylistsSerializer(playlist).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        playlist = self.get_object()
        return Response({
            "message": "Playlist retrieved successfully",
            "playlist": PlaylistsSerializer(playlist).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        playlist = self.get_object()
        name = playlist.name
        playlist.delete()
        return Response({
            "message": f"Playlist '{name}' has been deleted."
        }, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        playlist = self.get_object()
        serializer = self.get_serializer(playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Playlist has been updated",
            "playlist": PlaylistsSerializer(playlist).data
        }, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        playlist = self.get_object()
        
        if not request.user == playlist.author:
            return Response({
            "message": "Access Denied"
        }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(playlist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Playlist has been updated",
            "playlist": PlaylistsSerializer(playlist).data
        }, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = "username" 

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User created successfully",
            "user": UsersSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return Response({
            "message": "User retrieved successfully",
            "user": UsersSerializer(user).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        
        user.groups.clear()
        user.user_permissions.clear()
        
        image_field = getattr(user, 'image', None)
        if image_field and hasattr(image_field, 'path'):
            image_path = image_field.path
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"{e}")
        
        user.delete()
        return Response({
            "message": f"User '{username}' has been deleted."
        }, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        user = super().update(request, *args, **kwargs)
        return Response({
            "message": f"User '{user.data.get('username')}' has been updated" #type:ignore
        }, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs) 
        return Response({
            "message": f"User has been updated"
        }, status=status.HTTP_200_OK)
        
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongsSerializer
    lookup_field = "title" 

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        song = serializer.save(author=self.request.user)
        return Response({
            "message": "Song created successfully",
            "song": SongsSerializer(song).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        song = self.get_object()
        return Response({
            "message": "Song retrieved successfully",
            "song": SongsSerializer(song).data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        song = self.get_object()
        title = song.title
        
        image_field = getattr(song, 'image', None)
        if image_field and hasattr(image_field, 'path'):
            image_path = image_field.path
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"{e}")
                    
        song_field = getattr(song, 'song', None)
        if song_field and hasattr(song_field, 'path'):
            song_path = song_field.path
            if os.path.isfile(song_path):
                try:
                    os.remove(song_path)
                except Exception as e:
                    print(f"{e}")  
        
        song.delete()
        return Response({
            "message": f"Song '{title}' has been deleted."
        }, status=status.HTTP_200_OK)
        
    def update(self, request, *args, **kwargs):
        song = self.get_object()
        previous_image_path = song.image.path if song.image else None
        
        serializer = self.get_serializer(song, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        

        new_image_path = song.image.path if song.image else None
       
        if previous_image_path and previous_image_path != new_image_path:
            if os.path.isfile(previous_image_path):
                try:
                    os.remove(previous_image_path)
                except Exception as e:
                    print(f"{e}")
                    
        return Response({
            "message": "Song has been updated",
            "song": SongsSerializer(song).data
        }, status=status.HTTP_200_OK)
        
    def partial_update(self, request, *args, **kwargs):
        song = self.get_object()
        previous_image_path = song.image.path if song.image else None
        
        serializer = self.get_serializer(song, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        new_image_path = song.image.path if song.image else None
        if previous_image_path and previous_image_path != new_image_path:
            if os.path.isfile(previous_image_path):
                try:
                    os.remove(previous_image_path)
                except Exception as e:
                    print(f"{e}")
                    
        return Response({
            "message": "Song has been updated",
            "song": SongsSerializer(song).data
        }, status=status.HTTP_200_OK)