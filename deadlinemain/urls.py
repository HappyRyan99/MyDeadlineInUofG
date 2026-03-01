from django.urls import path
from .views import register_view, login_view  # 对应你的视图函数

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),  # 对应模板里的login链接
]
