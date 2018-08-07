from rest_framework import serializers

from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta():
        model = UserModel
        fields = ['id', 'username', 'password', 'tel', 'email', 'address', 'isDelete']