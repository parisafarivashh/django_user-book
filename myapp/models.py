from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError ("User must have an email address")

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email ,
            username,
            password = password

        )
        user.staff = True
        user.safe(using =self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password = password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)

        return user


class User(AbstractUser):

    email = models.EmailField(verbose_name='email addres', max_length=255, unique=True)
    username = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    object = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Dose the user have a specific permission?"""
        #simplest possible answer :yes ,always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff  """
        return self.staff

    @property
    def is_admin(self):
        """Is a user the admin member ? """
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

class Book(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
