from rest_framework.permissions import BasePermission, SAFE_METHODS



class CurriculumPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("lesson_questions", "questions"):
            return True
        return bool(request.method in SAFE_METHODS)
