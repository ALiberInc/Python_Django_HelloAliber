from django.urls import path, include
from django.contrib import admin
from . import views
from accounts.views import MyLoginView

app_name = 'profile_app'
urlpatterns = [
    path('', MyLoginView.as_view(),name="account_login"),
    path('employee_list', views.EmployeeListView.as_view(), name="employee_list"),
    path('employee/<int:pk>/', views.EmployeeView.as_view(), name="employee"),
    path('employee_delete/<int:id>/<int:user_id>', views.EmployeeDeleteView, name="employee_delete"),
    path('employee_set_active/<int:pk>/', views.EmployeeSetActiveView, name="employee_set_active"),
    path('employee_set_inactive/<int:pk>/', views.EmployeeSetInActiveView, name="employee_set_inactive"),
    path('employee_update/<int:pk>/', views.EmployeeUpdateView.as_view(), name="employee_update"),
    path('500', views.Test500View.as_view(), name="500"),
]
