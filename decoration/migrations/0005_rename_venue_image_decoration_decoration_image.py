# Generated by Django 5.0.1 on 2024-04-02 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decoration', '0004_remove_decoration_decoration_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='decoration',
            old_name='Venue_image',
            new_name='Decoration_image',
        ),
    ]
