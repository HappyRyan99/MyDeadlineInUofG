from django.urls import path

from . import views, api_views

urlpatterns = [

    path('', views.index, name='index'),  # Default to login

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('courses/', views.course_list, name='course_list'),
    path('groups/', views.my_groups, name='my_groups'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/', views.delete_course, name='delete_course'),
    path('edit_course/', views.edit_course, name='edit_course'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('api/dashboard_data/', api_views.dashboard_data, name='dashboard_data'),
    path('api/courses_data/', api_views.course_list_data, name='courses_data'),
    path('api/groups_data/', api_views.my_groups_data, name='groups_data'),

]
