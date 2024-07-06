import datetime

from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TodayVotesSerializer, VoteSerializer, RegistrationSerializer, EmployeeSerializer
from rest_framework import generics
from .models import Vote


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class TodayVotesViewSet(viewsets.ModelViewSet):
    serializer_class = TodayVotesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        today = datetime.date.today()
        queryset = Vote.objects.filter(date=today)
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_object(self):
        return self.request.user


class VoteViewSet(viewsets.ModelViewSet):
    today = datetime.date.today()
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteUpdateView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user: AbstractUser = self.request.user
        queryset = Vote.objects.all()

        if not user.is_staff:
            queryset = Vote.objects.filter(user=user)

        return queryset


