import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer, \
    TodayMenusSerializer
from rest_framework import generics


class RestaurantUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RestaurantSerializer
    lookup_field = "id"


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = MenuSerializer
    lookup_field = "id"


class MenuUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = MenuSerializer
    lookup_field = "id"


class TodayMenuViewSet(viewsets.ModelViewSet):
    serializer_class = TodayMenusSerializer
    lookup_field = "id"

    def get_queryset(self):
        today = datetime.date.today()
        queryset = Menu.objects.filter(date=today)
        return queryset
