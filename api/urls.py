from django.urls import path

from api.views import RegisterAPI , StudentView


urlpatterns = [ 
    
    path('register/', RegisterAPI.as_view(), name='register'),
    path('create_students/', StudentView.as_view(), name='register_student'),

    
]