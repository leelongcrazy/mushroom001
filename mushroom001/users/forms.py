from captcha.fields import CaptchaField
from django import forms
from users.models import UserInfo


class SignupForm(forms.Form):
    """
    用户注册信息表单
    """
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    work_id = forms.CharField(label="工号", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class LoginForm(forms.Form):
    """
    用户登录表单信息
    """
    username = forms.CharField(label="用户名/工号/邮箱",
                               max_length=128,
                               required=True,  # 必填字段
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密  码", required=True, min_length=6, max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               )  # 必填字段，最小长度6，最大长度20
    captcha = CaptchaField(label="验证码")

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #
    #     filter_result = User.objects.filter(username__exact=username)
    #     if not filter_result:
    #         raise forms.ValidationError("This username does not exist. Please register first.")
    #     return username
