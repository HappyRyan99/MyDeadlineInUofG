from django.urls import path
from . import views
from .views import register_view, login_view  # 对应你的视图函数

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('groups/', views.my_groups, name='my_groups'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/', views.delete_course, name='delete_course'),
    path('edit_course/', views.edit_course, name='edit_course'),

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),  # 对应模板里的login链接
]
