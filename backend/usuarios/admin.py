from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser


# UD5.1 - Administrador adaptado a los campos del usuario identificado por email.
@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ('email', 'username', 'activo', 'is_active', 'is_staff')
    list_filter = ('activo', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('create_date', 'update_date', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Datos personales', {'fields': ('username', 'first_name', 'last_name', 'activo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('create_date', 'update_date', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2', 'activo', 'is_active', 'is_staff')}),
    )
