from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


### Custom User Model Used Here

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


#### This is User Profile
class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=100, default='')
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, default='')
    mobile = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='users', default="/static/images/profile1.png", null=True, blank=True)
    bio = models.TextField(default='', blank=True)
    address = models.TextField(default='', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Category Model
class Category(models.Model):
	name = models.CharField(max_length=100, default='')
	image = models.ImageField(upload_to='categories', null=True, blank=True)
	primary = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


# Product Model
class  Product(models.Model):
    image = models.ImageField(upload_to='products', blank=True)
    title = models.CharField(max_length=300, default='')
    slug = models.SlugField()
    video = models.FileField(upload_to='videos', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Detail Text')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title



