# Generated by Django 5.1.3 on 2024-11-15 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_pet_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pet_images', to='chat.petsperson'),
        ),
    ]
