class Software(models.Model):
    name            = models.CharField(max_length=200, unique=True, verbose_name='Software Name')
    slug            = models.SlugField(unique=True, null=True)
    status          = models.BooleanField(default=False, verbose_name='Active')
    version         = models.CharField(max_length=300, verbose_name='Version', help_text='Version', blank=True, null=True)
    install_date    = models.CharField(max_length=300, verbose_name='Install Date', help_text='Install Date', blank=True, null=True)

    class Meta:
        verbose_name_plural = ('Software')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name


class Server(models.Model):
    name            = models.CharField(max_length=200, unique=True, verbose_name='Server Name')
    slug            = models.SlugField(unique=True, null=True)
    status          = models.BooleanField(default=False, verbose_name='Active')
    ip_address      = models.GenericIPAddressField(verbose_name='IP Address', blank=True, null=True)
    fqdn            = models.CharField(max_length=300, verbose_name='FQDN', help_text='FQDN', blank=True, null=True)
    
    software        = models.ManyToManyField(Software, verbose_name="Server Software", blank=True) # FOREIGN RELATIONSHIP to Software -> software_set

    class Meta:
        verbose_name_plural = ('Servers')
        ordering = ["id", "name"]

    def __str__(self):
        return self.name


class SoftwareSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Software
        fields = [
            'url',
            'id',
            'name',
            'version',
            'install_date'
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'name': {'validators': []},
        }

    def create(self, validated_data):
        software, created = Software.objects.update_or_create(
            name=validated_data.get('name', None),
            defaults={
                'name': validated_data.get('name', None),
                'version': validated_data.get('version', None),
                'install_date': validated_data.get('ip_address', None),
            })
        return software

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    software = SoftwareSerializer(many=True) # < - same here tried many ways 

    class Meta:
        model = Server
        fields = [
            'url',
            'id',
            'name',
            'status', 
            'ip_address', 
            'fqdn',
            'software' # <- I have tried software_set
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'name': {'validators': []}
        }

        depth = 1

    def create(self, validated_data):
        server, created = Server.objects.update_or_create(
            name = validated_data.get('name', None),
            defaults={
                'name': validated_data.get('name', None),
                'status': validated_data.get('status', None),
                'ip_address': validated_data.get('ip_address', None),
                'fqdn': validated_data.get('ip_address', None),
                #'software': # TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use software.set() instead.
            })
        return server


class SoftwareViewSet(viewsets.ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    lookup_field = 'slug'

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    lookup_field = 'slug'



        # software_items=validated_data.pop('software')
        # for software in software_items:
        #     print(software)
        #     # OrderedDict([('name', 'Software1'), ('version', '1.2.3')])
        #     # OrderedDict([('name', 'Software2')])