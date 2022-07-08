from django.db import models
from django.contrib.auth.models import User
from .util import *
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
# Create your models here.

class Category(models.Model):
	category_type = models.CharField(max_length=100)
	slug = models.SlugField(max_length=1000, null=True, blank=True)

	def __str__(self):
		return self.category_type

	def save(self , *args, **kwargs): 
		self.slug = generate_slug(self.category_type)
		super(Category, self).save(*args, **kwargs)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	image = models.ImageField(upload_to="images/blogs/")
	# summary = models.TextField(blank=True,null=True)
	summary = RichTextField(blank=True,null=True)
	summary_stripped = RichTextField(blank=True,null=True)
	slug = models.SlugField(max_length=1000, null=True, blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_date']

	def __str__(self):
		return self.title

	def save(self , *args, **kwargs): 
		if self.summary:
			self.summary_stripped = strip_tags(self.summary)
		self.slug = generate_slug(self.title)
		super(Post, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images/profiles/")


    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)