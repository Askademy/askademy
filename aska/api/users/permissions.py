from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class UserProfilePermission(BasePermission):
    def has_permission(self, request, view):
        http_method = request.method
        action = getattr(view, 'action', None)
        user = request.user

        if user.is_authenticated:
            if action == "create":
                return bool(http_method != "POST") # Only Unauthorized user can create an account
            elif action in ("update", "partial_update", "destroy", "suggested_friends"):
                return bool(user == view.get_object()) # # Allow these actions only to the user who owns the profile
            elif (action == "schools") and (http_method not in SAFE_METHODS):
                return bool(user == view.get_object())
            
            elif action == "friend_request":
                if http_method in ("POST", "PUT", "DELETE"):
                    return bool(user != view.get_object())
            return True
        
        elif action in ("list", "create"):
            return True        
        return False
        

