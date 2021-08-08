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


        depth = 1
