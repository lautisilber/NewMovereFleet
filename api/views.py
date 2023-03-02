from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import ApiTest
from .serializers import ApiTestSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def api_test(request: HttpRequest, format=None):

    if request.method == 'GET':
        api_tests = ApiTest.objects.all()
        serializer = ApiTestSerializer(api_tests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        print(type(request.data))
        serializer = ApiTestSerializer(data=request.data, many=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def api_test_id(request: HttpRequest, id: int, format=None):

    try:
        api_test = ApiTest.objects.get(pk=id)
    except ApiTest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApiTestSerializer(api_test)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ApiTestSerializer(api_test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        api_test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
