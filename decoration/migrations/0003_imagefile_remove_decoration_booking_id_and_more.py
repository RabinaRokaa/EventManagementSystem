# Generated by Django 5.0.1 on 2024-04-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decoration', '0002_decoration_booking_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='decorations/')),
            ],
        ),
        migrations.RemoveField(
            model_name='decoration',
            name='Booking_id',
        ),
        migrations.AlterField(
            model_name='decoration',
            name='Decoration_image',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='decorations/'),
        ),
    ]
