# Generated by Django 5.0.1 on 2024-04-02 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photographer', '0002_remove_photographer_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photographers/')),
            ],
        ),
        migrations.RemoveField(
            model_name='photographer',
            name='Image',
        ),
        migrations.AddField(
            model_name='photographer',
            name='Photographer_image',
            field=models.ManyToManyField(to='photographer.imagefile'),
        ),
    ]
