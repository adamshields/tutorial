from servers.models import Software, Server
from servers.serializers import SoftwareSerializer, ServerSerializer, MyServerSerializer, ServerSoftwareAPISerializer, ServerListAPIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'software': reverse('software-list', request=request, format=format),
        'servers': reverse('server-list', request=request, format=format)
    })

from rest_framework.generics import *
from rest_framework import status
from rest_framework.response import Response

class ServerSoftwareAPIView(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSoftwareAPISerializer
    lookup_field='slug'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        server_name = serializer.validated_data['name']
        exists = False
        if serializer.is_valid():
            try:
                # Check if server exists in database - true/false
                server_exists = Server.objects.filter(name=server_name).values_list('id', flat=True).exists()
                # server_id = Server.objects.filter(name=server_name).values_list('id', flat=True) # gets  id
                # print(server_exists)
                # print(server_id)
                if server_exists == False:
 
                    self.perform_create(serializer)
            except:
                server_exists = False
            # # server_name = serializer.data.get('name')
            # # self.perform_create(serializer)
            # print(server_name + '\n' + "Server Name ^^^ create ServerSoftwareAPIView ModelViewSet")
            return Response(data={'message': 'New Server Created ' + server_name})

    def perform_create(self, serializer):
        print("this perform_create")
        serializer.save()

    def partial_update(self, request):
        serialized = ServerSoftwareAPISerializer(data=request.data, partial=True)
        print('Partial')
        return Response(status=status.HTTP_202_ACCEPTED)


















    # # # # # # BACKUP STUFF
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     if serializer.is_valid():
    #         # server_name = serializer.data.get('name')
    #         server_name = serializer.validated_data['name']
    #         # self.perform_create(serializer)
    #         print(server_name + '\n' + "Server Name ^^^ create ServerSoftwareAPIView ModelViewSet")
    #         return Response(data={'message': 'New Server Created ' + server_name})
    #     else:
    #         return Response(data={'message': 'Server Exists already'}, status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
    #     print("this perform_create")
    #     serializer.save()










        #         # server_slug = serializer.validated_data['slug']
        #         # print(server_slug + '\n' + "Server Slug ^^^")
        #         # We need to get the server_name from the serialized data
        #         # 
        #         if server_name != '':
        #             server_list = Server.objects.filter(name=server_name)
        #             # self.perform_create(serializer)
        #             print('step1 create modelviewset')
        #             return Response(data={'message': 'New Server Created ' + server_name})
        #             # return Response(data={'message': 'New Server Created'}, status=status.HTTP_201_CREATED)
        #             if not server_list:
        #                 # server = serializer.save()
        #                 print('step2 create modelviewset \n')
        #                 return Response(data={'message': 'New Server Created ' + server_name})
        #                 # return Response(data={'message': 'New sadasd Created'}, status=status.HTTP_201_CREATED)
        #             else:
        #                 server = server_list[0]
        #                 serializer = ServerSoftwareAPISerializer(server)
        #                 print('step3 create modelviewset \n')
        #             return Response(serializer.data)   
        # else:
        #     return Response(data={'message': 'Server Exists already'}, status=status.HTTP_400_BAD_REQUEST)

        #         # self.perform_create(serializer)

        # # headers = self.get_success_headers(serializer.data)
        # # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
















    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     print("this perform_create")
    #     serializer.save()

    # def post(self,request,*args,**kwargs):
    #     serializer=NameSerializers(data=request.data)
    #     if serializer.is_valid:
    #         name=serializer.data.get('name')
    #         msg='Hello{}'.format(name)
    #         return Response({'msg':msg})
    #     else:
    #         return Response(serializer.errors,status=400)
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
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     # print(serializer)
    #     # serializer.is_valid(raise_exception=True)
    #     if serializer.is_valid():
    #             server_name = serializer.validated_data['name']
    #             print(server_name + '\n' + "Server Name ^^^ create modelviewset")
    #             # server_slug = serializer.validated_data['slug']
    #             # print(server_slug + '\n' + "Server Slug ^^^")
    #             if server_name != '':
    #                 server_list = Server.objects.filter(name=server_name)
    #                 # self.perform_create(serializer)
    #                 print('step1 create modelviewset')
    #                 # return Response(data={'message': 'New Server Created ' + server_name})
    #                 # return Response(data={'message': 'New Server Created'}, status=status.HTTP_201_CREATED)
    #                 if not server_list:
    #                     # server = serializer.save()
    #                     print('step2 create modelviewset \n')
    #                     return Response(data={'message': 'New Server Created ' + server_name})
    #                     # return Response(data={'message': 'New sadasd Created'}, status=status.HTTP_201_CREATED)
    #                 else:
    #                     server = server_list[0]
    #                     serializer = ServerSoftwareAPISerializer(server)
    #                     print('step3 create modelviewset \n')
    #                 return Response(serializer.data)   
    #     else:
    #         return Response(data={'message': 'Server Exists already'}, status=status.HTTP_400_BAD_REQUEST)

    #             # self.perform_create(serializer)

    #     # headers = self.get_success_headers(serializer.data)
    #     # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     print("this perform_create")
    #     serializer.save()

class ServerListAPIView(ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerListAPIView
    lookup_field = 'slug'

    def get_queryset(self):
        server = Server.objects.all()
        return server

    def post(self, request, *args, **kwargs):
        server_data = request.data
        print(f'This is :{server_data}')

        new_server = Server.objects.create(
            name=server_data['name'], 
            status=server_data['status'], 
            ip_address=server_data['ip_address'], 
            fqdn=server_data['fqdn'], 
            software=server_data['software'])

        new_server.save()

        serializer = ServerCreateUpdateSerializer(new_server)

        return Response(serializer.data)

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = ServerListAPIView(queryset, many=True)

    #     return Response(serializer.data)

    # # def get(self, request, *args, **kwargs):
    # #     print(f'This is {request.method} on SnippetDetail')
    # #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     print(f'This is {request.method} on SnippetDetail')
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     print(f'This is {request.method} on SnippetDetail')
    #     return self.destroy(request, *args, **kwargs)
# @csrf_exempt
# def my_server_list(request):
#     """
#     List all code servers, or create a new Server.
#     """
#     if request.method == 'GET':
#         servers = Server.objects.all()
#         # software = Software.objects.all()
#         serializer = MyServerSerializer(servers, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = MyServerSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def my_server_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         server = Server.objects.get(pk=pk)
#     except Server.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = MyServerSerializer(server)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = MyServerSerializer(server, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         server.delete()
#         return HttpResponse(status=204)

import logging
logger = logging.getLogger(__name__)

class SoftwareViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    lookup_field = 'slug'

    # def perform_create(self, serializer):
    #         if serializer.is_valid():
    #             software_name = serializer.validated_data['name']
    #             install_date = serializer.validated_data['install_date']

    #             if software_name != '':
    #                 product_list = Software.objects.filter(
    #                     product_name=software_name, product_location=install_date)

    #                 if not product_list:
    #                     print('test')
    #                     # product = create_product(product_name, product_location)
    #                 else:
    #                     product = product_list[0]

    #                 logger.info('product id : ' + str(product.id)) # Generated automatically
    #                 logger.info('product name : ' + product.product_name) # From the request
    #                 logger.info('product url : ' + product.product_url) # Generated by my create_product function

    #                 serializer = SoftwareSerializer(product)

    #                 # logger.info('serializer.data['id'] : ' + str(serializer.data['id']))
    #                 return Response(serializer.data)
    #             else:
    #                 return Response(data={'message': 'Empty product_name'}, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import serializers, request
class ServerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    lookup_field = 'slug'
    # serializer = serializer_class(request, context={'request': request})


    # def create(self, request, *args, **kwargs):
    #     server_data = request.data
    #     print(f'This is :{server_data}')          
    #     server_name = server_data['name']
    #     print(server_name)
    #     new_server = Server.objects.create(
    #         name=server_name, 
    #         slug=server_name.lower(), 
    #         status=server_data['status'], 
    #         ip_address=server_data['ip_address'], 
    #         fqdn=server_data['fqdn']
    #         # software=server_data['software']
    #         # software=software.set()
    #         # software=server_data.pop['software']
    #         )

    #     new_server.save()

    #     serializer = ServerCreateUpdateSerializer(new_server)

    #     return Response(serializer.data)

# from rest_framework import mixins, permissions
# from rest_framework.viewsets import GenericViewSet


# class Server2ViewSet(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  mixins.RetrieveModelMixin,
#                  GenericViewSet):
#     """
#     The following endpoints are fully provided by mixins:
#     * List view
#     * Create view
#     """
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer
#     lookup_field = 'slug'

# def retrieve(self, request, *args, **kwargs):
#     instance = self.get_object()
#     serializer = ServerSerializer(instance=instance)
#     return Response(serializer.data)


# from servers.models import Server
# from servers.serializers import ServerSerializer
# from rest_framework import mixins
# from rest_framework import generics

# class ServerList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer

#     def get(self, request, *args, **kwargs):
#         print(f'This is {request.method} on ServerList')
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         print(f'This is {request.method} on ServerList')
#         return self.create(request, *args, **kwargs)


# class ServerDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Server.objects.all()
#     serializer_class = ServerSerializer

#     def get(self, request, *args, **kwargs):
#         print(f'This is {request.method} on ServerDetail')
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         print(f'This is {request.method} on ServerDetail')
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         print(f'This is {request.method} on ServerDetail')
#         return self.destroy(request, *args, **kwargs)