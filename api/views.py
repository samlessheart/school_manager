from django.shortcuts import render
from rest_framework import generics, permissions, status
from api.serializers import RegisterSerializer, StudentRegisterSerializer
from rest_framework.response import Response
from .permissions import IsSchool
from main.models import Student
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):

        data = {'password':request.data.get('password')}

        serializer = self.get_serializer(request.user, data=data, partial = True)
        if serializer.is_valid():
            self.perform_update(serializer)

        return Response(serializer.data)
        

class StudentView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentRegisterSerializer
    permission_classes = [ IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many = True)
        serializer.is_valid(raise_exception= True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

