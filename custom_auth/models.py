from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """ Creates and saves a User with the given email, date of birth,
            and password. """

        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = MyUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """ Creates and saves a superuser with the given email, date of birth,
            and password. """

        u = self.create_user(
            username,
            email,
            password=password,
        )

        u.is_admin=True
        u.save(using=self._db)
        return u



class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    # Custom fields go here
    age = models.IntegerField(max_length=3, default=0)
    GENDER_CHOICES = ((0, 'Female'), (1, 'Male'), (2, 'Other'))
    gender = models.IntegerField(max_length=1, choices=GENDER_CHOICES, default=2)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
