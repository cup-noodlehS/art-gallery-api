import os
import sys
import django

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faso.settings')
django.setup()

from gallery.models import *
from myauth.models import *
import random
from django.db import transaction


def create_user():
    user_count = User.objects.count()
    location_ids = UserLocation.objects.values_list('id', flat=True)
    random_index = random.randint(0, len(location_ids) - 1)
    location = UserLocation.objects.get(id=location_ids[random_index])
    name = f"user_{user_count + 1}"
    user = User(
        email=f"{name}@gmail.com",
        username=name,
        password='123',
        user_type=User.BUYER,
        location=location
    )
    user.save()

def like_all_artworks():
    user = User.objects.first()
    artworks = Artwork.objects.all()
    for artwork in artworks:
        Like.objects.create(user=user, artwork=artwork)
        artwork.viewers_count += random.randint(100, 1000)
        artwork.save()

def follow_all_users():
    user = User.objects.first()
    users = User.objects.all()
    for user_to_follow in users:
        if user_to_follow != user:
            Following.objects.create(follower=user, followed=user_to_follow)

def create_bid_all():
    user = User.objects.first()
    artworks = Artwork.objects.all()
    for artwork in artworks:
        Bid.objects.create(user=user, artwork=artwork, bid_amount=random.randint(10000, 1000000))

if __name__ == '__main__':
    with transaction.atomic():
        create_user()
        like_all_artworks()
        follow_all_users()
        create_bid_all()

    print('Done')
