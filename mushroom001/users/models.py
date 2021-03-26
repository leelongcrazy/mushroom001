from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    identities = (
        (0, '代理商'),
        (1, '技术'),
        (2, '销售'),
        (3, '管理'),
        (4, '其他'),
    )
    identity = models.SmallIntegerField(choices=identities, default=4, verbose_name='用户分组')
    nick_name = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    birth_day = models.DateTimeField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女'),), default='男',
                              verbose_name="性别")
    address = models.CharField(max_length=100, blank=True, verbose_name='地址')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    work_id = models.SmallIntegerField(blank=True, verbose_name='工号', unique=True, null=True)
    join_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")
    image = models.ImageField(max_length=100, upload_to='images/%Y/%m', default='/images/default.png',
                              verbose_name='头像')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-join_time']
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
