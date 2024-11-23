from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

''''
class MyUser(models.Model):
    real_user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_pics', blank=True, null=True)

    
    def __str__(self):
        return self.real_user.username
'''

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("L'utilisateur doit avoir un nom d'utilisateur")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash le mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="user_images/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'  # Champ utilisé pour l'authentification
    REQUIRED_FIELDS = []  # Champs obligatoires lors de la création d'un superutilisateur

    def __str__(self):
        return self.username
