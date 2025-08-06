from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # when record is created
    updated_at = models.DateTimeField(auto_now=True)  # when record is last modified

    class Meta:
        abstract = True
