from rest_framework import serializers

from main.models import School, Student, CustomUser


class SchoolSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = School
        # fields = '['points', 'user']'
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = School
        # fields = '['points', 'user']'
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'is_school')
        extra_kwargs = {'password': {'write_only': True}, 'is_school': {'read_only':True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], 
                                              validated_data['email'], validated_data['password'], is_school = True)
        return user
    
    def update(self, instance, validated_data):
        instance.set_password = validated_data('password', instance.password )
        instance.save()
        return instance


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], 
                                              validated_data['email'], validated_data['password'], is_student = True)

        return user
