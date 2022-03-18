# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from panel.accounts.models import User

class EmailAuthBackend:
	"""
	Authenticate using e-mail account.
	"""
	def authenticate(self, request,email=None, password=None):
		try:
			user = User.objects.get(email=email)
			if user:
				if user.check_password(password):
					return user
			return None
		except get_user_model().DoesNotExist:
			try:
				user = User.objects.get(email=email, is_superuser=True)
				if user.check_password(password):
					return user
			except get_user_model().DoesNotExist:
				return None


	def get_user(self, user_id):
		try:
			return get_user_model().objects.get(pk=user_id)
		except get_user_model().DoesNotExist:
			return None
