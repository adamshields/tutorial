from rest_framework import serializers, request
from rest_framework.reverse import reverse
from servers.models import Server, Software
from drf_writable_nested.serializers import *




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
            'install_date',
            # 'server_set'
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
                'install_date': validated_data.get('install_date', None),
            })
        return software

#######################################
#               SERVER
#######################################

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    software = SoftwareSerializer(many=True, required=False)


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
            'url': {'lookup_field': 'slug'},
            'name': {'validators': []}
        }

        depth = 1



    # def create(self, validated_data):
    #     print(f'\n\nVALIDATED_DATA: \n\n{validated_data}')
    #     instance, _ = Server.objects.get_or_create(**validated_data)
    #     print(f'\n\nINSTANCE: \n\n{instance}')
    #     return instance


    def create(self,  validated_data):
        server = validated_data.get('name')
        print(server)
        status = validated_data.get('status')
        print(status)
        ip_address = validated_data.get('ip_address')
        print(ip_address)
        fqdn = validated_data.get('fqdn')
        print(fqdn)
        software = validated_data.pop('software')
        print(software)
        x = Software.objects.filter(name=self.validated_data['name']).exists()
        print(x.id)
        # instance = Software.objects.update_or_create(**validated_data)
        # instance.software = software
        # return instance
        # for software in software_items:
        #     print(software)
        # print(validated_data)
        server, created = Server.objects.update_or_create(
            name = validated_data.get('name', None),
            defaults={
                'name': validated_data.get('name', None),
                'status': validated_data.get('status', None),
                'ip_address': validated_data.get('ip_address', None),
                'fqdn': validated_data.get('ip_address', None),
                # 'software': {}# TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use software.set() instead.
            })
        # software_data = validated_data.pop('software')
        # # print(software_data)
        # # new_server = server
        # # print(new_server.name)
        # # print(new_server.status)
        # # print(new_server.ip_address)
        # # print(new_server.fqdn)
        # # a = new_server.software_set.set('software_data')
        # # server = Server.objects.create(
        # #     software=software['software'])
        # # print(a)
        # # server.add()
        # # for software in software_data:
        # #     print(software)
        # #     x = Software.objects.create(**software, server=server)
        # #     print(x)
        return server
        # # return new_server


        # new_server = Server.objects.create(
        #     name=server_data['name'], 
        #     status=server_data['status'], 
        #     ip_address=server_data['ip_address'], 
        #     fqdn=server_data['fqdn'], 
        #     software=server_data['software'])

        # new_server.save()

    #     serializer = ServerCreateUpdateSerializer(new_server)
    # def create(self, validated_data):
    #     print(f'this is data serializer: {validated_data}')
    #     if Software.objects.filter(name=self.validated_data['name']).exists():
    #         raise serializers.ValidationError("This software name already exists")
    #     return Software.objects.create(**validated_data)


        # if created == False:
        #     print(f'created is false \n server exists \n{validated_data}')
        #     print(f'created server \n{server}')
        #     return Server.objects.create(**validated_data)
        #     print(server)
        # else:
        #     print(f'created is true \n{validated_data}')
# As the error says, you're trying (indirectly) to set the software field as if it were a single field. 
# It's not, it's a RelatedManager, and you can't assign to a related manager in this way. Create your main server object, then assign the software via:

# server.software_set.set(...) # or .add(...) or whatever
# return Server.objects.update_or_create(name=server, **validated_data)
    # def create(self, validated_data):
    #     rate_hotels_data = validated_data.pop('rate_hotels')
    #     hotel_id = validated_data.pop('hotel_id')
    #     content_hotel, created = ContentHotel.objects.update_or_create(hotel_id=hotel_id, defaults={**validated_data})

    #     for rate_hotel_data in rate_hotels_data:
    #         rate_hotel_id = rate_hotel_data.pop('rate_hotel_id')
    #         RateHotel.objects.update_or_create(rate_hotel_id=rate_hotel_id, content_hotel=content_hotel,
    #                                            defaults=rate_hotel_data)
    # defaults={**validated_data}


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



class ServerSoftwareAPISerializer(serializers.HyperlinkedModelSerializer):
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
            'url': {'lookup_field': 'slug'},
            'name': {'validators': []},
            'slug': {'validators': []},
        }

        depth = 1

    def create(self, validated_data):
        print(f'SERIALIZER \n\n\n{validated_data}')
        print(f'\n\n\nSERIALIZER \n\n\n')
        # server_data = validated_data.pop['server']
        # print(server_data)
        software_data = validated_data.pop('software')
        # obj, created = Server.objects.update_or_create(
        #     name='John',
        #     defaults={'name': 'Bob'},
        # )
        server = Server.objects.create(**validated_data)
        # print(f'This is server name {server}')
        # print(f'This is software_data {software_data}')
        for software in software_data:
            print(software)
            Software.objects.create(**software, server=server)
        return server
        # Once you are done, create the instance with the validated data
        # return Server.objects.update_or_create(name=server, **validated_data)

    # def create(self, validated_data):
    #     print(f'this is data serializer: {validated_data}')
    #     if Software.objects.filter(name=self.validated_data['name']).exists():
    #         raise serializers.ValidationError("This software name already exists")
    #     return Software.objects.create(**validated_data)
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

# class ServerListAPIView(serializers.HyperlinkedModelSerializer):
#     software = SoftwareSerializer(many=True)
#     class Meta:
#         model = Server
#         fields = [
#             'url',
#             'id',
#             'name',
#             'status', 
#             'ip_address', 
#             'fqdn',
#             'software'
#             ]
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'}
#         }

#         depth = 1

# #######################################
# #               SERVER
# #######################################

# # class ServerSerializer(WritableNestedModelSerializer):
# # class ServerSerializer(serializers.ModelSerializer):
# class ServerSerializer(serializers.HyperlinkedModelSerializer):
# # class ServerSerializer(WritableNestedModelSerializer, serializers.HyperlinkedModelSerializer):

#     software = SoftwareSerializer(many=True, source='software_set')
#     # software = SoftwareSerializer(many=True, context={'request': request})
#     # software = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug') # shows associated slugs only
#     # software = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

#     class Meta:
#         model = Server
#         fields = [
#             'url',
#             'id',
#             'name',
#             # 'slug',
#             'status', 
#             'ip_address', 
#             'fqdn',
#             'software'
#             ]
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'},
#             'name': {'validators': []},
#             # 'software': {'validators': []},
#             # 'slug': {'validators': []},
#             # 'description': {'required': False},
#         }

#         depth = 1

#     def create(self, validated_data):
        
#         server, created = Server.objects.update_or_create(
#             name=validated_data.get('name', None),
#             defaults={
#                 'name': validated_data.get('name', None),
#                 'status': validated_data.get('status', None),
#                 'ip_address': validated_data.get('ip_address', None),
#                 'fqdn': validated_data.get('ip_address', None),
#                 'software': software_set,
#             })

#         return server
        
    # def create(self, validated_data):
    # # def create(self, instance, validated_data):
    #     software_data = validated_data.pop('software')
    #     print(software_data)
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={
    #             'name': validated_data.get('name', None),
    #             'status': validated_data.get('status', None),
    #             'ip_address': validated_data.get('ip_address', None),
    #             'fqdn': validated_data.get('ip_address', None),
    #         })
    #     return server
        # return super(ServerSerializer, self).create(instance, validated_data)

    # def update(self, instance, validated_data):
    #     # CHANGE "userprofile" here to match your one-to-one field name
    #     if 'software' in validated_data:
    #         nested_serializer = self.fields['software']
    #         nested_instance = instance.userprofile
    #         nested_data = validated_data.pop('software')

    #         # Runs the update on whatever serializer the nested data belongs to
    #         nested_serializer.update(nested_instance, nested_data)

    #     # Runs the original parent update(), since the nested fields were
    #     # "popped" out of the data
    #     return super(ServerSerializer, self).update(instance, validated_data)


# # You should already have this somewhere
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['nested', 'fields', 'you', 'can', 'edit']


# class UserSerializer(serializers.ModelSerializer):
#     # CHANGE "userprofile" here to match your one-to-one field name
#     userprofile = UserProfileSerializer()

#     def update(self, instance, validated_data):
#         # CHANGE "userprofile" here to match your one-to-one field name
#         if 'software' in validated_data:
#             nested_serializer = self.fields['software']
#             nested_instance = instance.userprofile
#             nested_data = validated_data.pop('software')

#             # Runs the update on whatever serializer the nested data belongs to
#             nested_serializer.update(nested_instance, nested_data)

#         # Runs the original parent update(), since the nested fields were
#         # "popped" out of the data
#         return super(ServerSerializer, self).update(instance, validated_data)



# defaults = {'first_name': 'Bob'}
# try:
#     obj = Person.objects.get(first_name='John', last_name='Lennon')
#     for key, value in defaults.items():
#         setattr(obj, key, value)
#     obj.save()
# except Person.DoesNotExist:
#     new_values = {'first_name': 'John', 'last_name': 'Lennon'}
#     new_values.update(defaults)
#     obj = Person(**new_values)
#     obj.save()
        # software, created = Software.objects.update_or_create(
        #     name=validated_data.get('name', None),
        #     defaults={
        #         'name': validated_data.get('name', None),
        #         'version': validated_data.get('version', None),
        #         'install_date': validated_data.get('ip_address', None),
        #     })
        # print(server)
        # for software in software_data:
        #     print(software)
        #     Software.objects.create(**software, server=server)
        # return software

        # def update(self, instance, validated_data):

        #     software_data = validated_data.pop('software')
        #     software = instance.software
        #     for k, v in software_data.items():
        #         setattr(software, k, v)
        #         software.save()
        #     for attr, value in validated_data.items():
        #         setattr(instance, attr, value)
        #         instance.save()
        #     return instance
        #     # if attr == 'assignees':
        #     #     instance.assignees.set(value)
        #     # else:
        #     #     setattr(instance, attr, value)
    # # THIS CREATES AND UPDATES SERVER NO PROBLEM BUT THROWS ERROR ON SOFTWARE    
    # def create(self, validated_data):
    #     server, created = Server.objects.update_or_create(
    #         name=validated_data.get('name', None),
    #         defaults={
    #             'name': validated_data.get('name', None),
    #             'status': validated_data.get('status', None),
    #             'ip_address': validated_data.get('ip_address', None),
    #             'fqdn': validated_data.get('ip_address', None),
    #         })
    #     return server

    # def create(self, validated_data):
    #     software_data = validated_data.pop('software')
    #     print(software_data)
    #     server = Server.objects.create(**validated_data)
    #     print(server)
    #     for software in software_data:
    #         print(software)
    #         Software.objects.create(**software, server=server)
    #     return server












                # 'software': validated_data.get(software.set()),
                # 'software': server.software.set(software),
                # 'software': validated_data.get(software.set('software'),
        # # server.software.set(software)
        # print(server)
        # # print(software_set)
        # return server

# id = 'some identifier that is unique to the model you wish to lookup'
# content_hotel, created = RateHotel.objects.get_or_create(
#     rate_hotel_id=rate_hotel_id, 
#     content_hotel=content_hotel, 
#     defaults=rate_hotel_data
# )

# if created:
#    # means you have created a new content hotel, redirect a success here or whatever you want to do on creation!
# else:
#    # content hotel just refers to the existing one, this is where you can update your Model


        # software, created = Software.objects.update_or_create(
        #     name=validated_data.get('name', None),
        #     defaults={
        #         'name': validated_data.get('name', None),
        #         'version': validated_data.get('version', None),
        #         'install_date': validated_data.get('install_date', None),
        #     })
        # return software
        # software_data = validated_data.pop('software')
        # print(f'This is software_data {software_data}')
        # for software in software_data:
        #     Software.objects.create(**software, server=server)
    #     # software_data = validated_data.pop('software')
    #     # print(f'This is software_data {software_data}')
    #     # software_models = []
    #     # for software in software_data:
    #     #     print(software)
    #     #     Software.objects.create(**software, server=server)
    #     # # server.software.set(software)
    #     return server





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