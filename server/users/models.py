from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from mutagen._file import File as AudioCheck

DEFAULT_IMAGE = "default/default_profile.jpg"

def get_image_url(instance, filename):
    return f"users_profile_pictures/{instance.username}/{filename}"

def get_song_image_url(instance, filename):
    return f"users_songs_pictures/{instance.author.username}/{filename}"

def get_song_url(instance, filename):
    return f"users_songs/{instance.author.username}/{filename}"

def validate_audio_file(value):
    try:
        audio = AudioCheck(value)
        if audio is None:
            raise ValidationError("Unsupported or invalid audio file.")
    except Exception:
        raise ValidationError("Invalid audio file.")

class Playlist(models.Model):
    title = models.CharField('Title', max_length=48, help_text='Max 48 symbols.')
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    songs = models.ManyToManyField('Song', related_name='Playlist')
    height = models.IntegerField(default=50, editable=False)
    width = models.IntegerField(default=50, editable=False)
    image = models.ImageField('Song Image', upload_to=get_song_image_url, default=DEFAULT_IMAGE, null=False, height_field='height', width_field='width')
    private = models.BooleanField('Privacy', default=True)

    def __str__(self) -> str:
        return f"{self.title} | Playlist"
    
class Song(models.Model):
    title = models.CharField('Title', max_length=48, help_text='Max 48 symbols.')
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    song = models.FileField('Audio File', upload_to=get_song_url, null=False, blank=False, validators=[validate_audio_file])
    height = models.IntegerField(default=50, editable=False)
    width = models.IntegerField(default=50, editable=False)
    image = models.ImageField('Song Image', upload_to=get_song_image_url, default=DEFAULT_IMAGE, null=False, height_field='height', width_field='width')
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username: str, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(
        "Username",
        null=False,
        unique=True,
        blank=False,
        max_length=64,
        help_text="Username has to be under 64 characters."
    )
    email = models.EmailField(
        "Email",
        unique=True,
        blank=False,
        null=False,
        help_text="Enter a valid email address"
    )
    joined_at = models.DateTimeField("Date joined", auto_now_add=True)
    height = models.IntegerField(default=50, editable=False)
    width = models.IntegerField(default=50, editable=False)
    image = models.ImageField(
        "Profile Image",
        height_field="height",
        width_field="width",
        upload_to=get_image_url,
        default=DEFAULT_IMAGE
    )
    is_banned = models.BooleanField(default=False)
    playlists = models.ManyToManyField('Playlist', related_name='Playlists')

    objects = UserManager() #type:ignore

    def __str__(self) -> str:
        return self.username

