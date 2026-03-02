from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('groups/', views.my_groups, name='my_groups'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/', views.delete_course, name='delete_course'),
    path('edit_course/', views.edit_course, name='edit_course'),

]
