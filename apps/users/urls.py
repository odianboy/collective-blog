from django.urls import path
from .views import UserDashboardView, UsersList, UserCard


urlpatterns = [
    # dashboard
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),

    #   users
    path('users_list/', UsersList.as_view(), name='users_list'),
    path('user_card/<int:pk>/', UserCard.as_view(), name='user_card'),
]
