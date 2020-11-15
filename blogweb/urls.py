from django.urls import path, include
from . import views
from .views import *
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post-created/', views.post_created, name='post-created'),
    path('post-detail/<id>/', views.post_detail, name='post-detail'),
    path('post-update/<id>/', views.post_update, name='post-update'),
    path('post-delete/<id>/', views.post_delete, name='post-delete'),
    
    #path('author-post/<str:username>', views.author_post, name='author-post'),
    path('author-post/<str:username>', UserPostListView.as_view(), name='author-post'),



]