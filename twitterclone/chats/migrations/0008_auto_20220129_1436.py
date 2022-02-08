# Generated by Django 3.2.9 on 2022-01-29 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0007_auto_20220129_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='recive_user',
            field=models.ManyToManyField(related_name='reciveuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chats',
            name='from_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fromuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
