# Generated by Django 5.0.4 on 2024-04-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]