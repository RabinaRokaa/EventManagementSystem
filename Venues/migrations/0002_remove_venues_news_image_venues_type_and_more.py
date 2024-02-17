# Generated by Django 5.0.1 on 2024-02-10 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venues', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venues',
            name='news_image',
        ),
        migrations.AddField(
            model_name='venues',
            name='Type',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='venues',
            name='Venue_image',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='venues/'),
        ),
    ]
