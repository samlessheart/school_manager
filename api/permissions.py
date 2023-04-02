from rest_framework import permissions

class IsSchool(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else :
            return request.user.is_school
        
class Isowner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        if request.user.is_school:
            return obj.school == request.user.school
        elif request.user.is_student:
            return obj == request.user.student 
        

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else :
            return request.user.is_student

class IsStafforSchool(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_school or request.user.is_staff