from rest_framework import serializers, request
from rest_framework.reverse import reverse
from servers.models import Server, Software
from drf_writable_nested.serializers import *




#######################################
#               SOFTWARE
#######################################


class SoftwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Software
        fields = [
            # 'url',
            'id',
            'name',
            'version',
            'install_date',
            # 'server_set',
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        # depth = 2

    def create(self, validated_data):
        print(f'this is data: {validated_data}')
        if Software.objects.filter(name=self.validated_data['name']).exists():
            raise serializers.ValidationError("This software name already exists")
        return Software.objects.create(**validated_data)


class ServerSoftwareAPISerializer(serializers.ModelSerializer):
    # software = SoftwareSerializer(many=True)
    class Meta:
        model = Server
        fields = [
            # 'url',
            'id',
            'name',
            'slug',
            'status', 
            'ip_address', 
            'fqdn',
            # 'software'
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
            # 'name': {'validators': []},
            # 'slug': {'validators': []},
        }

        depth = 1

    # def create(self, validated_data):
    #     print(f'{validated_data}')
    #     # server_data = validated_data.pop['server']
    #     # print(server_data)
    #     software_data = validated_data.pop('software')
    #     # obj, created = Server.objects.update_or_create(
    #     #     name='John',
    #     #     defaults={'name': 'Bob'},
    #     # )
    #     server = Server.objects.create(**validated_data)
    #     # print(f'This is server name {server}')
    #     # print(f'This is software_data {software_data}')
    #     for software in software_data:
    #         print(software)
    #         Software.objects.create(**software, server=server)
    #     return server
    #     # Once you are done, create the instance with the validated data
    #     return Server.objects.update_or_create(name=server, **validated_data)


# def perform_create(self, serializer):
#     if serializer.is_valid():
#         product_name = serializer.validated_data['product_name']
#         product_location = serializer.validated_data['product_location']

#         if product_name != '':
#             product_list = Product.objects.filter(
#                 product_name=product_name, product_location=product_location)

#             if not product_list:
#                 product = serializer.save()
#             else:
#                 product = product_list[0]
#                 serializer = ProductSerializer(product)
#             return Response(serializer.data)   
#         else:
#             return Response(data={'message': 'Empty product_name'},
#                         status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServerListAPIView(serializers.HyperlinkedModelSerializer):
    software = SoftwareSerializer(many=True)
    class Meta:
        model = Server
        fields = [
            'url',
            'id',
            'name',
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

#######################################
#               SERVER
#######################################

class ServerSerializer(WritableNestedModelSerializer):
# class ServerSerializer(serializers.ModelSerializer):
# class ServerSerializer(serializers.HyperlinkedModelSerializer):
# class ServerSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):

    # software = SoftwareSerializer(many=True)
    # software = SoftwareSerializer(many=True, context={'request': request})
    # software = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug') # shows associated slugs only
    # software = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

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
            # 'software'
            ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'name': {'validators': []},
            'slug': {'validators': []},
            # 'description': {'required': False},
        }

        depth = 1
    def create(self, validated_data):
        server, created = Server.objects.update_or_create(
            name=validated_data.get('name', None),
            defaults={
                'name': validated_data.get('name', None),
                'status': validated_data.get('status', None),
                'ip_address': validated_data.get('ip_address', None),
                'fqdn': validated_data.get('ip_address', None),
            })
        return server






# obj, created = sfs_upcs.objects.update_or_create(
#     # filter on the unique value of `upc`
#     upc=upc,
#     # update these fields, or create a new object with these values
#     defaults={
#         'product_title': product_title, 'is_buyable': is_buyable,  'price': price, 
#         'image_url': image_url, 'breadcrumb': breadcrumb, 'product_url': product_url,
#     }
# )
    # def create(self, validated_data):
    #     # server_name = validated_data['name']
    #     # if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == True:
    #     #     print(f'SERVER EXISTS IN DATABASE:')
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server
    # def create(self, validated_data):
    #     # server_name = validated_data['name']
    #     # if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == True:
    #     #     print(f'SERVER EXISTS IN DATABASE:')
    #     server, created = Server.objects.update_or_create(
    #         # slug = validated_data.get('name', None).lower(),
    #         name = validated_data.get('name', None),
    #         status = validated_data.get('status', None),
    #         ip_address = validated_data.get('ip_address', None),
    #         fqdn = validated_data.get('fqdn', None),
    #         defaults={
    #             'name': validated_data.get('name', None),
    #             # 'slug': validated_data.get('slug', None),
    #             'status': validated_data.get('status', None),
    #             'ip_address': validated_data.get('ip_address', None),
    #             'fqdn': validated_data.get('slug', None),

    #             })
    #     return server
    # def update(self, validated_data):
    #     server_name = validated_data['name']
    #     if Server.objects.filter(name=server_name).values_list('id', flat=True).exists() == False:
    #         print("Entry contained in queryset")
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server
    # def create(self, validated_data):
    #     server_name = validated_data['name']
    #     print(f'THIS IS VALIDATED DATA: \n ********** \n{validated_data}\n **********')
    #     # Check if server exists in database - and return true/false
    #     server_exists = Server.objects.filter(name=server_name).values_list('id', flat=True).exists()
    #     print(f'SERVER EXISTS IN DATABASE: \n ********** \n{server_exists}\n **********')
    #     if server_exists == False:
    #         print(f'CREATING NEW SERVER: \n{server_exists} with {server_name}')
    #         return Server.objects.create(**validated_data)
    #     else:
    #         print('WTF')
    # def create(self, validated_data):
    #     # incoming = data.'name')
    #     incoming = validated_data.get('name')
    #     if Server.objects.filter(name=incoming).exists():
    #         print("Entry contained in queryset")
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server

    # def update(self, instance, validated_data):
    #     server_data = validated_data.pop('name')
    #     # Unless the application properly enforces that this field is
    #     # always set, the following could raise a `DoesNotExist`, which
    #     # would need to be handled.
    #     server = instance.name

    #     instance.name = validated_data.get('name', instance.name)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.ip_address = validated_data.get('ip_address', instance.ip_address)

    #     instance.save()


    # def create(self, validated_data):
    #     # validate_name()
    #     print(f'{validated_data}')
    #     server_test = Server.objects.get(**validated_data)
    #     print(f'This is server name test with get {server_test}')

        
    #     server = Server.objects.create(**validated_data)
    #     print(f'This is created server name {server}')

        
    #     # software_data = validated_data.pop('software')
    #     # print(f'This is software_data {software_data}')
    #     # software_models = []
    #     # for software in software_data:
    #     #     print(software)
    #     #     Software.objects.create(**software, server=server)
    #     # # server.software.set(software)
    #     return server

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     server_name = serializer.validated_data['name']
    #     if serializer.is_valid():
    #         # Check if server exists in database - and return true/false
    #         server_exists = Server.objects.filter(name=server_name).values_list('id', flat=True).exists()
    #         print(f'Check if this server exists in database: \n{server_exists}')
    #         # If server does not exist create new server and call perform_create method
    #         if server_exists != True:
    #             print(f'This server does not exists in database lets create it: \n{server_exists}')
    #             self.perform_create(serializer)
    #             # return Response(data={'message': 'New Server Created ' + server_name})
    #         else:
    #             print(f'This server does exists in database lets update it: \n{server_exists}')
    #             # self.partial_update(serializer)
    #             # return Response(data={'message': 'Server Updated ' + server_name})

    # def create(self, validated_data):
    #     answer, created = Answer.objects.update_or_create(
    #         question=validated_data.get('question', None),
    #         defaults={'answer': validated_data.get('answer', None)})
    #     return answer
# this is self: ServerSerializer(context={'request': <rest_framework.request.Request: POST '/servers/'>, 'format': None, 'view': <servers.views.ServerViewSet object>}, 
# data={'name': 'aasasdasd', 'status': False}):
#     url = HyperlinkedIdentityField(lookup_field='slug', view_name='server-detail')
#     id = IntegerField(label='ID', read_only=True)
#     name = CharField(label='Server Name', max_length=200, validators=[<UniqueValidator(queryset=Server.objects.all())>])
#     status = BooleanField(label='Active', required=False)
# this is validated data: {'name': 'aasasdasd', 'status': False}
# this is the server slug: None
    # def create(self, validated_data):
    #     server_id = validated_data.get('server', None)
    #     if server_id is not None:
    #         server = Server.objects.filter(id=server_id).first()
    #         if server is not None:
    #             answer = server.answer
    #             if answer is not None:
    #                # update your answer
    #                return answer

    #     answer = Server.objects.create(**validated_data)
    #     return answer
    # def create(self, validated_data):
    #     # print(f'this is self: {self}')
    #     # print(f'this is validated data: {validated_data}')
    #     server_name = validated_data.get('name', None)
    #     print(f'this is the server name: {server_name}')
    #     # server_slug = validated_data.get('slug', None)
    #     # print(f'this is the server slug: {server_slug}')
    #     # server_id = validated_data.get('id', None),
    #     # print(f'this is the server slug: {server_id}')
    #     # if server_slug is not None:
    #     #     server = Server.objects.filter().first()
    #     #     return server
    #     #     print(server)
        
    #     server = Server.objects.create(**validated_data)
    #     print(f'this is server: {server}')
    #     return server

    # def create(self, validated_data):
    #     incoming = data.'name')
    #     # incoming = validated_data.get('name')
    #     if Server.objects.filter(name=incoming.name).exists():
    #         print("Entry contained in queryset")
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={'name': validated_data.get('name', None)})
    #     return server
    # def create(self, validated_data):
    #     try:
    #         self.instance = Software.objects.get(name=validated_data['name'])
    #         self.instance = self.update(self.instance, validated_data)
    #         assert self.instance is not None, (
    #             '`update()` did not return an object instance.'
    #         )
    #         return self.instance
    #     except Software.DoesNotExist:
    #         return super(SoftwareSerializer, self).create(validated_data)

            

    # def create(self, validated_data):
    #     if Software.objects.filter(name=self.validated_data['name']).exists():
    #         raise serializers.ValidationError("This software name already exists")
    #     return Software.objects.create(**validated_data)
    # def validate_name(self, value):
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Title is not about Django")
    #     return value
    # def create(self, validated_data):
    #     # validate_name()
    #     print(f'{validated_data}')
    #     server_test = Server.objects.get(**validated_data)
    #     print(f'This is server name test with get {server_test}')

        
    #     server = Server.objects.create(**validated_data)
    #     print(f'This is created server name {server}')

        
    #     software_data = validated_data.pop('software')
    #     print(f'This is software_data {software_data}')
    #     software_models = []
    #     for software in software_data:
    #         print(software)
    #         Software.objects.create(**software, server=server)
    #     # server.software.set(software)
    #     return server



    # def create(self, validated_data):
    #     softwares = validated_data.pop('software')
    #     software_models = []
    #     for sm in softwares:
    #         print("value of sm is: {}".format(sm))
    #         print("type of sm is: {}".format(type(sm)))
    #         new_software = Software.objects.create(sm)
    #         new_software.save()
    #         software_models.append(new_software)
    #     server = Server.objects.create(**validated_data)
    #     print(software_models)
    #     server.software.set(software_models)




    # def validate_name(self, value):
    #     print(value)
    #     if Server.objects.filter(name__contains=value).exists():
    #         raise serializers.ValidationError('Duplicate')
    #         return value

    # def validate_name(self, value):
    #     """
    #     Check that the blog post is about Django.
    #     """
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return value
    # """
    # server has software installed
    # """

    # def create(self, validated_data):
    #     software, created = Software.objects.get_or_create(
    #         server=validated_data.get('server', None),
    #         defaults={'software': validated_data.get('software', None)})

    #     return software

    # def create(self, validated_data):
    #     print(f'{validated_data}')
    #     # server_data = validated_data.pop['server']
    #     # print(server_data)
    #     software_data = validated_data.pop('software')
    #     server = Server.objects.create(**validated_data)
    #     print(f'This is server name {server}')
    #     print(f'This is software_data {software_data}')
    #     for software in software_data:
    #         print(software)
    #         Software.objects.create(**software, server=server)
    #     return server

    
    # def update(self, instance, validated_data):
    #     software_data = validated_data.pop('software')
    #     print(f'This is software_data {software_data}')
    #     instance.name = validated_data.get('name', instance.name)
    #     print(f'This is instance {instance}')
    #     instance.save()
        # return super().update(instance, validated_data)
# {'name': 'SERVER-588', 'status': True, 'ip_address': '249.125.196.238', 'fqdn': 'emil.com', 'software': [OrderedDict([('name', 's 3')]), OrderedDict([('name', 'asdfghsssjkl')])]}
# This is server name SERVER-588
# This is software_data [OrderedDict([('name', 's 3')]), OrderedDict([('name', 'asdfghsssjkl')])]
    # https://www.youtube.com/watch?v=EyMFf9O6E60
    # def create(self, validated_data):
    #     software_data = validated_data.pop('software')
    #     print(software_data)
    #     server = Server.objects.create(**validated_data)
    #     print(server)
    #     for software in software_data:
    #         print(software)
    #         Software.objects.create(**software, server=server)
    #     return server
    # def create(self, validated_data):
    #     choices = validated_data.pop('choices')
    #     tags = validated_data.pop('tags')
    #     question = Question.objects.create(**validated_data)
    #     for choice in choices:
    #         Choice.objects.create(**choice, question=question)
    #     question.tags.set(tags)
    #     return question
        
        # """
        # Create and return a new `Server` instance, given the validated data.
        # """
        # return Server.objects.create(**validated_data)

# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ['order', 'title', 'duration']

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']

#     def create(self, validated_data):
#         tracks_data = validated_data.pop('tracks')
#         album = Album.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album




    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.code = validated_data.get('code', instance.code)
    #     instance.linenos = validated_data.get('linenos', instance.linenos)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.style = validated_data.get('style', instance.style)
    #     instance.save()
    #     return instance
    # def create(self, validated_data):
    #     print(request.data)
    #     software_data = validated_data.pop('software')
    #     print(software_data)
    #     server = Server.objects.create(**validated_data)
    #     for software_data in softwaress_data:
    #         Server.objects.create(software=software, **software_data)
    #     return server

class MyServerSerializer(serializers.ModelSerializer):

    # software = SoftwareSerializer(context = {'request':request},data=request.data)

    class Meta:
        model = Server
        fields = [
            # 'url',
            'id',
            'name',
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


# python manage.py shell
# from servers.serializers import SoftwareSerializer, ServerSerializer
# serializer = ServerSerializer()
# print(repr(serializer))