from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['login', 'pas', 'mail']

    def validate(self, data):
        existing_record = Users.objects.filter(login=data['login']).first()
        if existing_record:
            raise serializers.ValidationError('A record with the same Username already exists.')
        existing_record = Users.objects.filter(mail=data['mail']).first()
        if existing_record:
            raise serializers.ValidationError('A record with the same mail already exists.')
        return data