from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError("All the fields haven't been adequately filled")
        if not password:
            raise ValueError("All the fields haven't been adequately filled - password")

        user_obj = self.model(
            email=self.normalize_email(email),
        )

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# Create your user models here.
class Users(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)

    # django defaults
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    # django default functions
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Notes(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    note = models.CharField(max_length=10000, default='')
    date = models.DateTimeField(auto_now_add=True)
