# Generated by Django 5.0.4 on 2024-05-18 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0013_featuredartowrk_added_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featuredartowrk',
            options={'ordering': ['added_on']},
        ),
    ]
