from django.urls import path
from .views import RestaurantViewSet, RestaurantUpdateView, MenuViewSet, \
    TodayMenuViewSet, MenuUpdateView

urlpatterns = [
    path('restaurants/', RestaurantViewSet.as_view({'get': 'list'}), name='restaurant_list'),

    path('restaurant/add/', RestaurantViewSet.as_view({'post': 'create'}, ), name='restaurant_create'),
    path('restaurant/<int:id>/', RestaurantUpdateView.as_view(), name='restaurant_update'),

    path('menu/<int:id>/', MenuUpdateView.as_view(), name='menu_update'),

    path('menu/', MenuViewSet.as_view({'post': 'create'}), name='menu_create'),
    path('menu/all/', TodayMenuViewSet.as_view({'get': 'list'}), name='menu_today_list'),
]