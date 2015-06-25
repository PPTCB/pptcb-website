from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom UserManager for the User model.

    This allows the email field to be the 'username'.
    """
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given first/last names, email and password.
        """
        now = timezone.now()
        if not first_name:
            raise ValueError('The given first name must be set')
        if not last_name:
            raise ValueError('The given last name must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name,
                          email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """
        Creates a standard user.
        """
        return self._create_user(first_name, last_name, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
        Creates a superuser.
        """
        return self._create_user(first_name, last_name, email, password, True, True,
                                 **extra_fields)