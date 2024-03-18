from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate
from .models import NewsStory
from django.http import QueryDict
from .serializers import NewsStorySerializer
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


def Greet(request):
    if request.method == 'GET':
        return HttpResponse("Welcome to Adham Hamza News Agency", status=status.HTTP_200_OK)
    else:
        return HttpResponse("This Endpoint only allows GET requests", status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['POST'])
def Login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({"message": "Successful login.",
                                "token": token.key}, 
                                content_type='text/plain', 
                                status=status.HTTP_200_OK)
        else:
            return HttpResponse('Error: Invalid username or password.',
                                content_type='text/plain',
                                status=status.HTTP_401_UNAUTHORIZED)
    else:
        return HttpResponse('Error: This endpoint only supports POST requests.',
                            content_type='text/plain',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    if request.method == 'POST':
            try:
                token = Token.objects.get(user=request.user)
            except Token.DoesNotExist:
                return HttpResponse('Error: User not logged in.', status=status.HTTP_503_SERVICE_UNAVAILABLE)
            logout(request)
            token.delete()
            return Response({"message": "Successful Logout.",
                                "token": token.key}, status=status.HTTP_200_OK)
    else:
        return HttpResponse('This endpoint only supports POST requests.', 
                            content_type='text/plain', 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def Story(request):
    # Post Story
    if request.method == 'POST':
        try:
            serializer = NewsStorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return HttpResponse("Story posted successfully", serializer.data, status=status.HTTP_201_CREATED)
            return HttpResponse("Error: Could not post story", serializer.errors, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except PermissionDenied:
            return HttpResponse("Error: Permission Denied.", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    # Get Stories
    elif request.method == 'GET':
        category = request.query_params.get('story_cat', '*')
        region = request.query_params.get('story_region', '*')
        date = request.query_params.get('story_date', '*')
        filter_conditions = {}
        try:
            if category != '*':
                filter_conditions['category__icontains'] = category
            if region != '*':
                filter_conditions['region__icontains'] = region
            if date != '*':
                    filter_conditions['date__gte'] = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            return HttpResponse("Invalid Data Entered.", status=status.HTTP_404_NOT_FOUND)
                
        stories = NewsStory.objects.filter(**filter_conditions)
        
        serialized_stories = [{
            'key': story.id,
            'headline': story.headline,
            'story_cat': story.category,
            'story_region': story.region,
            'author': story.author.username,
            'story_date': story.date.strftime('%d/%m/%Y'),
            'story_details': story.details
        } for story in stories]
        if serialized_stories:            
            return JsonResponse({'stories': serialized_stories}, status=status.HTTP_200_OK)
        else:
            return HttpResponse("No Stories Found.", 
                                content_type='text/plain',
                                status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse('This endpoint only supports POST or GET requests.', 
                                content_type='text/plain', 
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteStory(request, key):
    if request.method == 'DELETE':
        try:
            story = NewsStory.objects.get(id=key)
            story.delete()
            return HttpResponse(f"Story {key} deleted successfully.", 
                                content_type='text/plain',
                                status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return HttpResponse(f'The story with key {key} does not exist.',
                                content_type='text/plain',
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return HttpResponse("This method only accepts DELETE requests", 
                                content_type='text/plain',
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)