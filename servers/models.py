from django.conf import settings
from django.urls import reverse
from django.db import models

from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

#######################################
#               SOFTWARE
#######################################

class Software(models.Model):
    name            = models.CharField(max_length=200, unique=True, verbose_name='Software Name')
    slug            = models.SlugField(unique=True, null=True)
    status          = models.BooleanField(default=False, verbose_name='Active')
    version         = models.CharField(max_length=300, verbose_name='Version', help_text='Version', blank=True, null=True)
    install_date    = models.CharField(max_length=300, verbose_name='Install Date', help_text='Install Date', blank=True, null=True)

    class Meta:
        verbose_name = ('Software')
        verbose_name_plural = ('Software')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("software_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
	    return reverse("software_update", kwargs={"slug": self.slug})

def pre_save_software(sender, instance, *args, **kwargs):
	slug = slugify(instance.name)
	instance.slug = slug

pre_save.connect(pre_save_software, sender=Software)

#######################################
#               SERVER
#######################################

class Server(models.Model):
    name            = models.CharField(max_length=200, unique=True, verbose_name='Server Name')
    slug            = models.SlugField(unique=True, null=True)
    status          = models.BooleanField(default=False, verbose_name='Active')
    ip_address      = models.GenericIPAddressField(verbose_name='IP Address', blank=True, null=True)
    fqdn            = models.CharField(max_length=300, verbose_name='FQDN', help_text='FQDN', blank=True, null=True)

    # FOREIGN RELATIONSHIP to Software software_set
    software        = models.ManyToManyField(Software, verbose_name="Server Software", blank=True)

    class Meta:
        verbose_name = ('Server')
        verbose_name_plural = ('Servers')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("server_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
	    return reverse("server_update", kwargs={"slug": self.slug})
        

def pre_save_server(sender, instance, *args, **kwargs):
	slug = slugify(instance.name)
	instance.slug = slug
    
pre_save.connect(pre_save_server, sender=Server)
