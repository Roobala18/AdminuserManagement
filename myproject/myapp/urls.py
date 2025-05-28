from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Add logout
    #admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-projects/', views.projects_page, name='projects_page'),
    path('admin-employees/', views.employees_page, name='employees_page'),
    path('admin-tasks/', views.tasks_page, name='tasks_page'),
    path('admin-productivity/', views.productivity_page, name='productivity_page'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/edit/<int:user_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:user_id>/', views.delete_employee, name='delete_employee'),
    # path('projects/create/', views.create_project, name='create_project'),
    # path('projects/', views.projects_page, name='project_page'),
    path('admin-dashboard/projects/', views.project_list, name='project_list'),
    path('admin-dashboard/projects/add/', views.add_project, name='add_project'),
    #user
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),

]
