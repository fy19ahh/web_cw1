# Generated by Django 5.0.2 on 2024-03-10 21:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsStory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')], max_length=10)),
                ('region', models.CharField(choices=[('uk', 'UK'), ('eu', 'Europe'), ('w', 'World')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(max_length=128)),
                ('author', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
