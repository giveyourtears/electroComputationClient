from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, FilialForm, PsForm
from .models import AskueUser, FilialModel, PSModel


# Register your models here.

class AskueUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('username', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'fullname', 'filter_department', 'inhibit_filter')}),
        ('Права доступа', {'fields': ('is_admin', 'edit_permission', 'is_staff')})
    )
    search_fields = ('username', 'filter_department')
    ordering = ('username', 'filter_department')

    filter_horizontal = ()


class FilialAdmin(admin.ModelAdmin):
    add_form = FilialForm
    fieldsets = (
        (None, {'fields': ('short_name', 'full_name')}),
    )


class PsAdmin(admin.ModelAdmin):
    add_form = FilialForm
    fieldsets = (
        (None, {'fields': ('short_name', 'full_name')}),
    )


admin.site.register(AskueUser, AskueUserAdmin)
admin.site.register(FilialModel, FilialAdmin)
admin.site.register(PSModel, PsAdmin)
admin.site.unregister(Group)
