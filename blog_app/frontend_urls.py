from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/<int:pk>/', views.blog_detail_view, name='blog-detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('create/', views.create_post_view, name='create-post'),
]
