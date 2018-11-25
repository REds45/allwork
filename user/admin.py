from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm,UserChangeForm


class UserAdmin(BaseUserAdmin):
    # 定义修改和添加表单
    form = UserChangeForm
    add_form = UserCreationForm

    # 用于显示用户模型的字段
    # 这些会覆盖原本UserAdmin的定义
    list_display = ('email', 'is_admin', 'is_active',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)})
    )

    # add_fieldsets不是标准的ModelAdmin属性
    # UserAdmin会在创建时使用此属性覆盖掉get_fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# 组成自己写的User和UserAdmin
admin.site.register(User, UserAdmin)
# 因为我们自己设计了用户权限，没有使用Django内建的权限机制，所以在这里从admin中注销Group
admin.site.unregister(Group)

