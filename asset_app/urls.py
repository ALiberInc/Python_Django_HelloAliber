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
    path('asset_create_done',views.create_done_view,name="ASS003_asset_create_done"),
    path('asset/<int:pk>/',views.AssetView.as_view(),name="asset"),
    path('asset/<int:pk>/<str:model_name>/',views.AssetView.as_view(),name="asset"),
    path('asset/department/get/', views.ajax_get_department, name='ajax_get_department'),
    path('asset/post', views.post, name="post"),
    path('asset/lifecycle/<str:asset_id>/', views.AssetLifeCycleView.as_view(), name="asset_lifecycle"),
]