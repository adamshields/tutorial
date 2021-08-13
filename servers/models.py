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

    # def get_absolute_url(self):
    #     return reverse("software_detail", kwargs={"slug": self.slug})

    # def get_update_url(self):
	#     return reverse("software_update", kwargs={"slug": self.slug})

def pre_save_software(sender, instance, *args, **kwargs):
	slug = slugify(instance.name)
	instance.slug = slug

pre_save.connect(pre_save_software, sender=Software)

# #######################################
# #        SERVER MODEL MANAGER
# #######################################
# class ServerManager(models.Manager):


#     # def create(self, username, email, is_premium_member=False, has_support_contract=False):
#     #     user = User(username=username, email=email)
#     #     user.save()
#     #     profile = Profile(
#     #         user=user,
#     #         is_premium_member=is_premium_member,
#     #         has_support_contract=has_support_contract
#     #     )
#     #     profile.save()
#     #     return user

#     def create(self, name, slug):
#         server = Server(name=name, slug=slug)
#         print(server)
#         server.save()
#         software = Software(
#             name='name'
#         )
#         software.save()
#         return server


# {
#     "name": "Server20",
#     "status": true,
#     "ip_address": "1.22.1.4",
#     "fqdn": "server1.domain.com",
#     "software": [
#         {
#             "name": "Python 3.6.6",
#             "version": "3.6.6",
#             "install_date": "02242021"
#         },
#         {
#             "name": "Java 1.7.281",
#             "version": "1.7.281",
#             "install_date": "04042020"
#         }
#     ]
# }



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

    # objects = ServerManager()

    class Meta:
        verbose_name = ('Server')
        verbose_name_plural = ('Servers')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name

    @property
    def soft(self):
        return self.software_set.all()

    def get_absolute_url(self):
        return reverse("server_detail", kwargs={"slug": self.slug})

    # def get_update_url(self):
	#     return reverse("server_update", kwargs={"slug": self.slug})

    def get_primary_key(self):
	    return reverse("server_detail", kwargs={"id": self.id})   

def pre_save_server(sender, instance, *args, **kwargs):
	slug = slugify(instance.name)
	instance.slug = slug
    
pre_save.connect(pre_save_server, sender=Server)
