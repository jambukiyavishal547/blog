# urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, BlogCreateView, BlogListView, BlogEditView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/edite/', BlogEditView.as_view(), name='blog_edite'),
]