from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Get a permission based on model and codename
def get_permission(model: models.Model, codename: str) -> Permission:
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    return permission
