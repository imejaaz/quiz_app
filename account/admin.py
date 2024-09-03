from django.contrib import admin

from django.contrib import admin
from .models import User


from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'is_active',
        'is_staff', 'is_superuser', 'country', 'created_by', 'role'
    )


admin.site.register(User, UserAdmin)
