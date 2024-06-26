# Generated by Django 5.0.4 on 2024-05-01 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_alter_artwork_buyer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artwork',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-bid_amount']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['sent_on']},
        ),
        migrations.AlterModelOptions(
            name='messagethread',
            options={'ordering': ['-created_on']},
        ),
        migrations.CreateModel(
            name='FeaturedArtowrk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featured_on', models.DateTimeField(auto_now_add=True)),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.artwork')),
            ],
            options={
                'ordering': ['-featured_on'],
            },
        ),
    ]
