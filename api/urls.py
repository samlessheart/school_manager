from django.urls import path

from api.views import  AddStudentAPI, AddSchoolAPI, Students, updatestudent, Schools, AddGrade, StudentDetail
from rest_framework_simplejwt.views import (    TokenObtainPairView,    TokenRefreshView)

urlpatterns = [ 
    
    path('students/', Students.as_view(), name='students'),
    path('student/<int:pk>/', StudentDetail.as_view(), name='studentsdetail'),
    path('addstudent/', AddStudentAPI.as_view(), name='addstudent'),
    path('addschool/', AddSchoolAPI.as_view(), name='addschool'),
    path('updatestudent/<int:pk>/', updatestudent, name='updatestudent'),
    path('schools/', Schools.as_view(), name='schools'),
    path('addgrade/', AddGrade.as_view(), name='addgrade'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
]