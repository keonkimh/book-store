from django.db import models
from core.models.base import BaseModel


class BookGenre(BaseModel):
    name: str = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.name)
