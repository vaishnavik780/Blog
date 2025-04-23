from django.urls import path
from .views import *
urlpatterns = [
    path('',login_view, name='login'),
    path('post_list', post_list, name='post_list'),
    path('register_view/',register_view, name='register_view'),
    path('logout_view/',logout_view, name='logout_view'),
    path('post_create/', post_create, name='post_create'),
    path('post_delete/<int:id>', post_delete, name='post_delete'),
    path('update_post/<int:id>', update_post, name='update_post'),
    path('comment/<int:post_id>/', Comment, name='Comment'), 
    path('only/<int:id>/',only, name='only'),
    
    #path('', PostListView.as_view(), name='post_list'),
]