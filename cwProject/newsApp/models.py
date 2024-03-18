from django.db import models
from django.contrib.auth.models import User
import uuid


class NewsStory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    headline = models.CharField(max_length=64)
    
    categories = [('pol', 'Politics'), 
                  ('art', 'Art'),
                  ('tech', 'Technology'),
                  ('trivia', 'Trivia')]
    category = models.CharField(max_length=10, choices=categories)
    
    regions = [('uk', 'UK'),
               ('eu', 'Europe'),
               ('w', 'World')]
    region = models.CharField(max_length=10, choices=regions)
    author = models.ForeignKey(User, max_length=30, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=128)
    
    def __str__(self):
        return self.headline
    
