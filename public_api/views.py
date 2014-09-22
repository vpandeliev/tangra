"""
view.py

Primarily responsible for accepting POST object via the url. DataView will
accept a request. If the request is sent via POST, DataView will attempt to
put the data into Data table.
"""

from django.shortcuts import render
from django.db import connection
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from serializers import *


class DataView(APIView):
    """
    Add a new record into Data Table.
    """
    
    renderer_classes = (JSONRenderer,)
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication,
                              authentication.BasicAuthentication)
    #permission_classes = (permissions.IsAdminUser,)

    
    def post(self, request, format=None):
        """
        Update the data onto the database.
        """
        
        serializer = DataSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)