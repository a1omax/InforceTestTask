from django.urls import path
from .views import RegistrationAPIView, TodayVotesViewSet, ProfileViewSet, VoteViewSet, VoteUpdateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('registration/', RegistrationAPIView.as_view(), name='registration'),

    path('profile/', ProfileViewSet.as_view({'get': 'retrieve'}), name='profile'),

    path('today-votes/', TodayVotesViewSet.as_view({'get': 'list'}), name='result_list'),
    path('vote/', VoteViewSet.as_view({'post': 'create'}), name='vote_create'),
    path('vote/<int:id>/', VoteUpdateView.as_view(), name='vote_update'),

]
