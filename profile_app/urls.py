from django.urls import path, include
from django.contrib import admin
from . import views
from accounts.views import MyLoginView

app_name = 'profile_app'
urlpatterns = [
    path('', MyLoginView.as_view(),name="account_login"),
    path('department_list', views.DepartmentListView.as_view(), name="department_list"),
    path('department_create', views.DepartmentCreateView.as_view(), name="department_create"),
    path('department_update/<int:pk>/', views.DepartmentUpdateView.as_view(), name="department_update"),
    path('validate_department/get', views.validate_department,
    name='validate_department'),
    path('check_delete_department/get', views.check_delete_department,
    name='check_delete_department'),
    path('department_delete/<int:pk>/', views.DepartmentDeleteView, name="department_delete"),
    path('employee_list', views.EmployeeListView.as_view(), name="employee_list"),
    path('employee/<int:pk>/', views.EmployeeView.as_view(), name="employee"),
    path('employee_delete/<int:id>/<int:user_id>', views.EmployeeDeleteView, name="employee_delete"),
    path('employee_set_active/<int:pk>/', views.EmployeeSetActiveView, name="employee_set_active"),
    path('employee_set_inactive/<int:pk>/', views.EmployeeSetInActiveView, name="employee_set_inactive"),
    path('employee_update/<int:pk>/', views.EmployeeUpdateView.as_view(), name="employee_update"),
    path('500', views.Test500View.as_view(), name="500"),
]
