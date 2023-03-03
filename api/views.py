from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .utils import get_all_serializers_from_module
from api import serializers
from main import serializers
from user import serializers

api_serializers = get_all_serializers_from_module('api.serializers')
main_serializers = get_all_serializers_from_module('main.serializers')
user_serializers = get_all_serializers_from_module('user.serializers')
all_serializers = api_serializers | main_serializers | user_serializers
all_models = { k:v.Meta.model for k, v in all_serializers.items() }


@api_view(['GET', 'POST'])
def getpost(request: HttpRequest, url_name: str, format=None):

    if request.user.profile.position_type < 3:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if url_name not in all_serializers:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer_class = all_serializers[url_name]
    model_class = all_models[url_name]

    # query params
    many = False
    if 'many' in request.GET:
        if request.GET['many'].lower() == 'true':
            many = True
    prefetch = []
    if 'children' in request.GET:
        prefetch = request.GET['children']
        if not isinstance(prefetch, list): prefetch = [prefetch]
    # filter = None TODO: think o how to add support for this

    if request.method == 'GET':
        query = model_class.objects
        for rel in prefetch: # TODO: see if this works
            query.prefetch_related(rel)
        model = query.all() if many else query.first()
        serializer = serializer_class(model, many=many)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = serializer_class(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def getputdelete(request: HttpRequest, url_name: str, id: int, format=None):

    if request.user.profile.position_type < 3:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if url_name not in all_serializers:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer_class = all_serializers[url_name]
    model_class = all_models[url_name]

    # query params
    prefetch = []
    if 'children' in request.GET:
        prefetch = request.GET['children']
        if not isinstance(prefetch, list): prefetch = [prefetch]

    try:
        query = model_class.objects
        for rel in prefetch: # TODO: see if this works
            query.prefetch_related(rel)
        model = query.get(pk=id)
    except model_class.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializer_class(model)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = serializer_class(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
