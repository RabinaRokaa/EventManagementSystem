# Generated by Django 5.0.1 on 2024-02-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0004_rename_venue_images_venues_venue_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venues',
            name='Venue_image',
        ),
        migrations.AddField(
            model_name='venues',
            name='Venue_image',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='venues/'),
        ),
    ]
