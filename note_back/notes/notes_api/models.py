from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = "1")
    title = models.CharField(max_length=200, blank=True, null = True)
    content = models.TextField(max_length=500, blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id} {self.title} {self.user}"
