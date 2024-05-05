from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'avatar_url',
                    'phone_number', 'location', 'user_type', 'user_type_display', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'avatar_url', 'user_type_display']