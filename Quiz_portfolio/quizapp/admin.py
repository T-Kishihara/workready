from django.contrib import admin
from .models import (
    Quiz, Choices
)


admin.site.register(
    [Quiz, Choices]
)