from rest_framework import serializers
from django.db import transaction
from main.models import Grades, School, Student, CustomUser

class Schoolserializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, style={'input_type': 'password'},  write_only= True)
    email = serializers.EmailField()
    name =  serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=6)

    @transaction.atomic
    def create(self, validated_data):
        user = CustomUser.objects.create(username = validated_data['username'], 
                                         email = validated_data['email'],
                                         password =validated_data['password'], is_school = True )
        user.set_password(validated_data['password'])
        school = School.objects.create(name = validated_data['name'], city = validated_data['city'],                                        
                                       pincode = validated_data['pincode'],user = user )
        user.save()
        school.save()
        return validated_data


def not_a_grade(value):
    try:
        Grades.objects.get(grade = value)
        return value
    except:
        raise serializers.ValidationError('This grade is not there yet')


class StudentSerializer(serializers.Serializer):    
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, style={'input_type': 'password'},  write_only= True)
    name =  serializers.CharField(max_length=100)
    grade = serializers.IntegerField(validators = [not_a_grade])
    school = serializers.StringRelatedField()
    
    @transaction.atomic
    def create(self, validated_data):
        
        user = CustomUser.objects.create(username = validated_data['username'], 
                                        password =validated_data['password'] , is_student = True)
        user.set_password(validated_data['password'])
        student = Student.objects.create(name = validated_data['name'], grade = Grades.objects.get(grade =validated_data['grade']), 
                                user = user, school = validated_data['school']    )
        user.save()
        student.save()
        return validated_data


class BaseStudentSerializer(serializers.ModelSerializer):
    school = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    class Meta:
        model = Student
        fields = '__all__'


class BaseSchoolSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = School
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'