import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Employee
from .models import Vote
import django.contrib.auth.password_validation as validators


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=Employee.objects.all(),
                                                               message="Email already exists")])
    username = serializers.CharField(max_length=50, min_length=5, validators=[
        UniqueValidator(queryset=Employee.objects.all(), message="Username already exists")])
    password = serializers.CharField(max_length=256, min_length=1, write_only=True, )

    class Meta:
        model = Employee
        fields = [
            'email',
            'username',
            'password',
        ]

    def validate_password(self, value):
        validators.validate_password(value)
        return value

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)


class TodayVotesSerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = [
            'user',
            'restaurant'
        ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'id',
            'restaurant',
            'date'
        ]

    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data['user'] = request.user
        validated_data['date'] = datetime.date.today()
        votes = Vote.objects.filter(user=request.user, date=datetime.date.today())
        if not votes.exists():
            return Vote.objects.create(**validated_data)

        vote = votes.first()
        vote.restaurant = validated_data['restaurant']
        vote.save()
        return vote


class EmployeeSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('username', 'email', 'votes')

    def get_votes(self, obj):
        votes = Vote.objects.filter(user=obj)
        return VoteSerializer(votes, many=True).data
