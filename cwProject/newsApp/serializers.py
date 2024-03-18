from rest_framework import serializers
from .models import NewsStory

class NewsStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsStory
        fields = ['id', 'headline', 'category', 'region', 'details', 'author', 'date']
        read_only_fields = ['author', 'date']