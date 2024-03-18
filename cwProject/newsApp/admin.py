from django.contrib import admin
from  .models import NewsStory

class StoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'date')

admin.site.register(NewsStory, StoryAdmin)
