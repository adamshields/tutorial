from servers.models import Software, Server
from servers.serializers import SoftwareSerializer, ServerSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'software': reverse('software-list', request=request, format=format),
        'servers': reverse('server-list', request=request, format=format)
    })

class SoftwareViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer


class ServerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
