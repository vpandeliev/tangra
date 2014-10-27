from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):

    def create_user(self, username, email, date_of_birth, password=None):
        """ Creates and saves a User with the given email, date of birth,
            and password. """

        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = MyUserManager.normalize_email(email),
            date_of_birth = date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """ Creates and saves a superuser with the given email, date of birth,
            and password. """

        u = self.create_user(
            username,
            email,
            password=password,
            date_of_birth=date_of_birth
        )

        u.is_admin=True
        u.save(using=self._db)
        return u



class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
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
