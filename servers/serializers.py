from rest_framework import serializers
from rest_framework.reverse import reverse
from servers.models import Server, Software


#######################################
#               SOFTWARE
#######################################


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
            'url': {'lookup_field': 'slug'}
        }


#######################################
#               SERVER
#######################################

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    software = SoftwareSerializer(many=True)
    class Meta:
        model = Server
        fields = [
            'url',
            'id',
            'name',
            # 'slug',
            'status', 
            'ip_address', 
            'fqdn',
            'software'
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

        depth = 1
