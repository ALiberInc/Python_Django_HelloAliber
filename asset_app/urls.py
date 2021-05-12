from django.urls import path

from . import views

app_name = 'asset_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('product_list', views.ProductListView.as_view(), name="product_list"),
    path('product_create', views.ProductCreateView.as_view(), name="product_create"),
    path('product_update/<int:pk>/', views.ProductUpdateView.as_view(), name="product_update"),
    path('product_delete/<int:pk>/',views.ProductDeleteView, name="product_delete"),
    path('asset_list',views.AssetListView.as_view(), name="asset_list"),
    path('asset_create',views.AssetCreateView.as_view(),name="asset_create"),
]