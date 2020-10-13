from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'profile_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('employee_list', views.EmployeeListView.as_view(), name="employee_list"),
    path('employee', views.EmployeeView.as_view(), name="employee"),
    path('employee2/<int:pk>/', views.EmployeeView2.as_view(), name="employee2"),
    path('employee_detail/<int:pk>/', views.EmployeeDetailView.as_view(), name="employee_detail"),
    path('employee_update/<int:pk>/', views.EmployeeUpdateView.as_view(), name="employee_update"),
]
