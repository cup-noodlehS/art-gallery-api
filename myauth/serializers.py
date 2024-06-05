from rest_framework import serializers
from .models import User, UserLocation

class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['id', 'name', 'user_count']
        extra_kwargs = {'user_count': {'read_only': True}}

class SimpleUserLocationSerializer(serializers.ModelSerializer):
    class Meta(UserLocationSerializer.Meta):
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    is_banned = serializers.BooleanField(read_only=True)
    location = SimpleUserLocationSerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    followers_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'avatar_url',
                    'phone_number', 'location', 'user_type', 'user_type_display',
                    'about', 'achievements', 'is_banned', 'password', 'location_id',
                    'followers_count']
        extra_kwargs = {'password': {'write_only': True},
                        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'avatar_url', 'user_type_display', 'followers_count']