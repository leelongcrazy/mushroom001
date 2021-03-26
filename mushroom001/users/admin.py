from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserInfo


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'work_id', 'email', 'gender', 'address', 'mobile',
                    'join_time', 'is_staff'
                    )
    list_filter = ('username', 'work_id', 'mobile')
    search_fields = ("username", "work_id")
    list_per_page = 20

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        # 设置管理员和超级管理员可以更改账号是否员工状态
        if request.user.is_superuser or '管理员' in group_names:
            return 'is_staff',
        return ()

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g)
        return group_names

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(UserInfoAdmin, self).get_changelist_instance(request)

    # 设置后台管理 修改也页面信息展示
    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields': (
            "username", "work_id", 'email', 'gender', 'birth_day',
            ('address', 'mobile'), ('groups', 'identity'),
            ('is_staff', 'is_active'))}),
        )
