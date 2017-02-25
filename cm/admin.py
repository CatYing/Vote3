from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from cm.models import *
# Register your models here.


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member)
admin.site.register(Record)
