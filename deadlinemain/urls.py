from django.urls import path
from .views import views, api_views, login_views, dashboard_views, course_views, group_views

urlpatterns = [

    path('', dashboard_views.index, name='index'),  # Default to login

    path('register/', login_views.register_view, name='register'),
    path('login/', login_views.login_view, name='login'),
    path('logout/', login_views.logout_view, name='logout'),

    path('courses/', course_views.course_list, name='course_list'),
    path('groups/', group_views.my_groups, name='my_groups'),
    path('add_course/', course_views.add_course, name='add_course'),
    path('delete_course/', course_views.delete_course, name='delete_course'),
    path('edit_course/', course_views.edit_course, name='edit_course'),

    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('add_task/', dashboard_views.add_task, name='add_task'),
    path('delete_task/', dashboard_views.delete_task, name='delete_task'),
    path('api/dashboard_data/', api_views.dashboard_data, name='dashboard_data'),
    path('api/courses_data/', api_views.course_list_data, name='courses_data'),
    path('api/groups_data/', api_views.my_groups_data, name='groups_data'),

]
