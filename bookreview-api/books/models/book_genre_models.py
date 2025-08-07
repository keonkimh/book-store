from django.db import models
from core.models.base import BaseModel

class BookGenre(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
