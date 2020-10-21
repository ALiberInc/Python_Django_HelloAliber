from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'profile_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('employee_list', views.EmployeeListView.as_view(), name="employee_list"),
    path('employee/<int:pk>/', views.EmployeeView.as_view(), name="employee"),
    path('employee_delete/<int:pk>/', views.EmployeeDeleteView, name="employee_delete"),
]
