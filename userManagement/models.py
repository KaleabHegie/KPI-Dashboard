from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be specified')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        extra_fields = {
            'is_staff': True,
            'is_superuser': True,
        }
        return self.create_user(email, username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    user_image = models.ImageField(
        upload_to='profile_image', blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="last login", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_sector = models.BooleanField(default=False)
    is_mopd = models.BooleanField(default=False)
    is_hopr = models.BooleanField(default=False)
    is_dpg = models.BooleanField(default=False)
    is_ess = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email


class ResponsibleMinistry(models.Model):
    responsible_ministry_eng = models.CharField(max_length=350)
    responsible_ministry_amh = models.CharField(
        max_length=350, blank=True, null=True)
    code = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.responsible_ministry_eng}"


class UserSector(models.Model):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True)
    user_sector = models.ForeignKey(
        ResponsibleMinistry, on_delete=models.CASCADE)
    
