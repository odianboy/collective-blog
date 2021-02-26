from django.urls import path
from apps.blog.views import (
    Index, CategoryPosts, UserPublicationDetailView, UserPostEdit, UserPostDelete, UserPostNew, UserPublicationView
)


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<int:pk>', CategoryPosts.as_view(), name='category'),
    path('dashboard/publications/',  UserPublicationView.as_view(), name='publications'),

    # publications
    path('publications/<int:pk>/',  UserPublicationDetailView.as_view(), name='post_user_detail'),
    path('publications/<int:pk>/edit/', UserPostEdit.as_view(), name='post_user_edit'),
    path('publications/<int:pk>/delete/', UserPostDelete.as_view(), name='post_user_delete'),
    path('publications/new/', UserPostNew.as_view(), name='post_user_new'),
]
