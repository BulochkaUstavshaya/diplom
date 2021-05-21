from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, username, password, **extra_fields):

        # Create and save a user with the given username, email and password.

        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            email=email, username=username, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, username, password, **extra_fields
        )

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email, username, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class SetOfClothes(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    name_Set_Of_Clothes = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.users)


class Clothes(models.Model):
    set_Of_Clothes = models.ManyToManyField(SetOfClothes)
    name_Clothes = models.CharField(max_length=50)
    type_Clothes = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    link_Image = models.URLField(max_length=255)
    link_Source = models.URLField(max_length=255, unique=True)

    def __str__(self):
        return self.link_Source

    class Meta:
        verbose_name = 'Clothes'
        verbose_name_plural = 'Clothes'

# OLD WORKING VERSION

# from django.core.mail import send_mail
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.db import models
# from django.utils.translation import ugettext_lazy as _
#
# from django.contrib.auth.base_user import BaseUserManager
#
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#     def _create_user(self, email, username, password, **extra_fields):
#
#         # Create and save a user with the given username, email and password.
#
#         if not email:
#             raise ValueError('The given email must be set')
#         if not username:
#             raise ValueError('The given username must be set')
#
#         email = self.normalize_email(email)
#         username = self.model.normalize_username(username)
#         user = self.model(
#             email=email, username=username, **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(
#             email, username, password, **extra_fields
#         )
#
#     def create_superuser(self, email, username, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(
#             email, username, password, **extra_fields
#         )
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         validators=[username_validator],
#     )
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     # created_at = models.DateTimeField(auto_now_add=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         send_mail(subject, message, from_email, [self.email], **kwargs)
#
#
# class UserClothes(models.Model):
#     users = models.ManyToManyField(User)
#     nameClothes = models.CharField(max_length=50)
#     typeClothes = models.CharField(max_length=100)
#     description = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=9, decimal_places=2)
#     linkImage = models.URLField(max_length=255)
#     linkSource = models.URLField(max_length=255, unique=True) # unique=True
#
#     def __str__(self):
#         # return self.nameClothes
#         return self.linkSource
#
#     class Meta:
#         verbose_name = 'Clothes'
#         verbose_name_plural = 'Clothes'
