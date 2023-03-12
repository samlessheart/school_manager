from django.db import models
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)


class School(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique= True, null= True)
    city = models.CharField(max_length=50, null= True)
    pincode = models.CharField(max_length=6, null=True )

# @receiver(post_save, sender=CustomUser)
# def create_school_user(sender, instance, created , **kwargs):
#     if created and instance.is_school:
#         School.objects.create(user = instance, **kwargs)




class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(School,  on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    grade = models.IntegerField()


# @receiver(post_save, sender=CustomUser)
# def create_student_user(sender, instance, created , **kwargs):
#     if created and instance.is_student:
#         Student.objects.create(user = instance, **kwargs)
