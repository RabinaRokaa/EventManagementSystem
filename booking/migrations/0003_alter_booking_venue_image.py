# Generated by Django 5.0.1 on 2024-04-20 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_booking_venue_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='Venue_image',
            field=models.ImageField(blank=True, null=True, upload_to='venues/'),
        ),
    ]
