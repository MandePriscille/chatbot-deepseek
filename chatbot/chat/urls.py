from django.urls import path
from . import views


urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('create/', views.conversation_create, name='conversation_create'),
    path('detail/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('delete/<int:conversation_id>/', views.conversation_delete, name='conversation_delete'),
]