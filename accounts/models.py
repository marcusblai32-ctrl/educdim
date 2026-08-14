from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_year, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, birth_year=birth_year, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, birth_year, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, birth_year, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True, blank=True, verbose_name="ID unique")
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, verbose_name="Prénom")
    last_name = models.CharField(max_length=30, verbose_name="Nom")
    birth_year = models.PositiveIntegerField(verbose_name="Année de naissance")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nimewo telefòn")
    receive_email_notifications = models.BooleanField(default=True, verbose_name="Resevwa notifikasyon pa imel")
    receive_sms_notifications = models.BooleanField(default=False, verbose_name="Resevwa notifikasyon pa SMS")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Nouvo champs pou swiv aktivite
    last_activity = models.DateTimeField(default=timezone.now, verbose_name="Dernière activité")
    notification_sent = models.BooleanField(default=False, verbose_name="Notification envoyée")
    notification_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de notification")
    delete_scheduled = models.BooleanField(default=False, verbose_name="Suppression programmée")
    delete_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_year']

    def save(self, *args, **kwargs):
        if not self.user_id:
            prefix = f"{self.last_name[:1].upper()}{self.first_name[:1].upper()}{str(self.birth_year)[-2:]}"
            while True:
                candidate = f"{prefix}-{uuid.uuid4().hex[:6].upper()}"
                if not CustomUser.objects.filter(user_id=candidate).exists():
                    self.user_id = candidate
                    break
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_activity(self):
        """Mete ajou dènye aktivite a"""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

    def is_inactive(self, days=90):
        """Verifye si kont inaktif depi 90 jou"""
        delta = timezone.now() - self.last_activity
        return delta.days > days

    def should_be_deleted(self):
        """Verifye si kont dwe efase (4 mwa san aktivite apre notifikasyon)"""
        if not self.delete_scheduled or not self.delete_date:
            return False
        return timezone.now() > self.delete_date