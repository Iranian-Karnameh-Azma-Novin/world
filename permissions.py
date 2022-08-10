from rest_framework.permissions import BasePermission, SAFE_METHODS
#from .models import UserExchange , Exchange

class IsOwnerOrReadOnly(BasePermission):
	message = 'permission denied, you are not the owner'

	def has_permission(self, request, view):
		if request.user.is_authenticated :
			return True
		else : print("permission denied")

	def has_object_permission(self, request, view, UserExchange):
		if UserExchange.user == request.user:
			return True


#		if vacation_obj.owner.id == request.user.id:


class admin(BasePermission):
	message = 'permission denied, you are not the owner'

	def has_permission(self, request, view):
		if request.user.is_authenticated :
			return True
		else : print("hi")

	def has_object_permission(self, request, view):
		if user.is_superuser:
			return True
