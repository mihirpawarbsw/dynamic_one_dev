# models.py
from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User model

class UserAuthentication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to auth_user
    email = models.EmailField()
    token = models.CharField(max_length=255)

    def __str__(self):
        return f"User ID: {self.user.id}, Email: {self.email}, Token: {self.token}"

    class Meta:
        db_table = 'user_authentication'  # Ensure this matches your manually created table name
