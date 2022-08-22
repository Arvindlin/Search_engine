from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
    """Model for Data"""
    id_search = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField()
    code = models.TextField()
    project = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_created')
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_update')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(blank=True, default=[])

    def __str__(self):
        return str(self.title)
