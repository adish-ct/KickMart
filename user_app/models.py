from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from .utils import generate_referal_code


# app : user_app

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True, default="{% static "
                                                                                         "'img/none_user.jpg' %}")
    date_of_birth = models.DateField(blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    wallet = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Custom User'

    def __str__(self):
        return '{}'.format(self.email)
    


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    alternative_mobile = models.IntegerField(blank=True)
    address = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=150, null=False)
    zip_code = models.IntegerField(null=False)
    nearby_location = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=150, null=False)
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.email}"
    

class PasswordControl(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    forgot_password_token = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    referal_code = models.CharField(max_length=12, blank=True, null=True)
    refered_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='referrals')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name}-{self.referal_code}"

    def get_recommened_profiles(self):
        pass

    def save(self, *args, **kwargs):
        if self.referal_code == "":
            code = generate_referal_code()
            self.referal_code = code
        super().save(*args, **kwargs)


    
    

