from django.db import models
from django.utils.translation import gettext_lazy as _


class Server(models.Model):
    name            = models.CharField(max_length=200, unique=True, verbose_name='Server Name')
    slug            = models.SlugField(unique=True, null=True)
    status          = models.BooleanField(default=False, verbose_name='Active')
    ip_address      = models.GenericIPAddressField(verbose_name='IP Address', blank=True, null=True)
    fqdn            = models.CharField(max_length=300, verbose_name='FQDN', help_text='FQDN', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('server')
        verbose_name_plural = _('servers')

    def get_absolute_url(self):
        return f'/server/{self}/'



class Software(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('name'))
    slug = models.SlugField(unique=True, null=True)
    # server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='servers', verbose_name=_('server'))
    server = models.ManyToManyField(Server, verbose_name="Server Software", blank=True)
    year = models.IntegerField(verbose_name=_('year'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('software')
        verbose_name_plural = _('software')

    def get_absolute_url(self):
        return f'/server/{self.server}/{self}/'


class Version(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name=_('name'))
    slug = models.SlugField(unique=True, null=True)
    index = models.IntegerField(verbose_name=_('index'))
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='versions', verbose_name=_('software'))
    duration = models.CharField(max_length=255, db_index=False, null=True, blank=True, verbose_name=_('duration'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('index',)
        verbose_name = _('version')
        verbose_name_plural = _('versions')
