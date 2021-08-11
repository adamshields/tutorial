import django.contrib.auth
from django.db import models
from django.conf import settings

class Profile(models.Model):
    display_name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = ('Profile')
        verbose_name_plural = ('Profiles')
        ordering = ["id", "display_name"]

    def __str__(self):
        return self.display_name
        
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, related_name='listings', null=True, on_delete=models.SET_NULL)
    owners = models.ManyToManyField(
        Profile,
        related_name='owned_listings',
        db_table='profile_listing',
        blank=True
    )
    class Meta:
        verbose_name = ('Listing')
        verbose_name_plural = ('Listings')
        ordering = ["id", "title"]

    def __str__(self):
        return self.title