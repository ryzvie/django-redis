from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    #path('authuser/', views.authuser, name='authuser'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('test', views.test_notification, name='test-notif'),
    #path('action/copy-pipeline/<int:id>/', views.action_copy_pipeline, name='copy-pipeline'),
    
]
