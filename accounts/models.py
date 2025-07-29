from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.UserRole.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with roles for TingGo platform
    """
    class UserRole(models.TextChoices):
        ADMIN = 'admin', _('Administrator')
        ORGANIZER = 'organizer', _('Event Organizer')
        PARTICIPANT = 'participant', _('Event Participant')
        VENDOR = 'vendor', _('Vendor/Partner')
        HOST = 'host', _('Experience Host')
    
    # Basic fields
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    
    # Role and status
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PARTICIPANT,
        verbose_name=_('user role')
    )
    is_verified = models.BooleanField(default=False, verbose_name=_('verified'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    
    # Profile information
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    
    # Location and preferences
    country = models.CharField(_('country'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Español'),
            ('ht', 'Kreyòl Ayisyen'),
        ],
        default='en',
        verbose_name=_('preferred language')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Username not required
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Optional. 150 characters or fewer.'),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_organizer(self):
        return self.role == self.UserRole.ORGANIZER
    
    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN
    
    @property
    def is_vendor(self):
        return self.role == self.UserRole.VENDOR
    
    @property
    def is_host(self):
        return self.role == self.UserRole.HOST


class UserProfile(models.Model):
    """
    Extended profile information for users
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Social media links
    website = models.URLField(_('website'), blank=True)
    instagram = models.CharField(_('instagram'), max_length=100, blank=True)
    facebook = models.CharField(_('facebook'), max_length=100, blank=True)
    twitter = models.CharField(_('twitter'), max_length=100, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True, verbose_name=_('email notifications'))
    push_notifications = models.BooleanField(default=True, verbose_name=_('push notifications'))
    
    # For organizers and vendors
    business_name = models.CharField(_('business name'), max_length=200, blank=True)
    business_description = models.TextField(_('business description'), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"Profile for {self.user.email}"
