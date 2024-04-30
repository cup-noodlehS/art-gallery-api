# Generated by Django 5.0.4 on 2024-04-30 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gallery', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artworks_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artwork',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='artworks_bought', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artworkimage',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.artwork'),
        ),
        migrations.AddField(
            model_name='bid',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.artwork'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='artwork',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gallery.category'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_message_threads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='artwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.artwork'),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_message_threads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.messagethread'),
        ),
    ]