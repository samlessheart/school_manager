from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False, editable=False)
    is_school = models.BooleanField(default=False, editable=False)


class School(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique= True, null= True)
    city = models.CharField(max_length=50, null= True)
    pincode = models.CharField(max_length=6, null=True )

    def __str__(self) -> str:
        return self.name

# @receiver(post_save, sender=CustomUser)
# def create_school_user(sender, instance, created , **kwargs):
#     if created and instance.is_school:
#         School.objects.create(user = instance, **kwargs)

def grade_valid(grade):
    if grade > 0:
        return grade
    else:
        raise ValidationError("Grade should be greater than 0")


class Grades(models.Model):
    grade = models.IntegerField(primary_key=True, validators=[grade_valid])


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grades, null =True, on_delete=models.SET_NULL, )

    def __str__(self) -> str:
        return self.name

# @receiver(post_save, sender=CustomUser)
# def create_student_user(sender, instance, created , **kwargs):
#     if created and instance.is_student:
#         Student.objects.create(user = instance, **kwargs)

