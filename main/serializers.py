from rest_framework import serializers
from .models import *


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = "__all__"


class BookingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookings
        fields = "__all__"


class ChattingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chattings
        fields = "__all__"
