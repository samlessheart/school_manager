from django.shortcuts import render
from rest_framework import generics, permissions, status
from api.serializers import  BaseSchoolSerializer, Schoolserializer, StudentSerializer, BaseStudentSerializer, GradeSerializer
from rest_framework.response import Response
from .permissions import IsSchool, IsStudent, Isowner
from main.models import CustomUser, Student, School
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes


class AddSchoolAPI(generics.GenericAPIView):
    serializer_class = Schoolserializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)

class AddStudentAPI(generics.GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [ IsAuthenticated, IsSchool]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(school = request.user.school)
        return Response(serializer.data)


class Students(generics.GenericAPIView):
    serializer_class = BaseStudentSerializer
    permission_classes = [ IsAuthenticated]
    def get_queryset(self):
        grade = self.request.query_params.get('grade', None)
        school = self.request.query_params.get('school', None)        
        queryset = Student.objects.all()
        if self.request.user.is_school:
            queryset = queryset.filter(school = self.request.user.school)
        elif self.request.user.IsAdminUser and school is not None:
            queryset.filter(school = school)

        if grade is not None:
            queryset = queryset.filter(grade = grade)
        return queryset        

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many =True)
        return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsStudent, IsSchool])
def updatestudent(request, pk):    
    student = Student.objects.get(id = pk)
    serializer = BaseStudentSerializer(student)
    err_msg = {"detail": "You do not have permission to perform this action."}
    if request.method == "PUT":
        if request.user.is_school:
            if student.school != request.user.school :
                return Response( err_msg, status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.is_student:
            if student != request.user:
                return Response(err_msg, status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get('name'):
            student.name = request.data['name']
            # student.user.username = request.data['name']
        if request.data.get('password'):        
            student.user.set_password(request.data['password'])

        student.save()
        student.user.save()
        return Response(serializer.data)
    

class Schools(generics.GenericAPIView):
    serializer_class = BaseSchoolSerializer

    def get_queryset(self):        
        queryset = School.objects.all()        
        return queryset        
    
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many =True)
        return Response(serializer.data)


class AddGrade(generics.GenericAPIView):
    serializer_class = GradeSerializer
    permission_classes = [ IsAuthenticated, IsAdminUser]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StudentDetail(generics.RetrieveAPIView):
    serializer_class = BaseStudentSerializer
    permission_classes = [IsAuthenticated, Isowner]
    queryset = Student.objects.all()

