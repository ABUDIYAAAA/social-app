# Generated by Django 3.2.9 on 2022-01-28 09:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chats', models.ManyToManyField(blank=True, related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
