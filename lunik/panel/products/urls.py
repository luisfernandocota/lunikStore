from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('add', views.add_product, name='add_product'),
    path('edit/<str:product_slug>', views.edit_product, name="edit_product"),
    path('add/size', views.add_size, name='add_size'),
    path('add/color', views.add_hexacode, name='add_hexacodes'),
    path('info/<str:product_slug>', views.info_product, name='info_product'),
    path('delete/<str:product_slug>', views.delete_product, name="delete_product"),
    path('delete/product/<str:product_slug>/image/<int:pk>', views.delete_product_image, name="delete_product_image"),

    #-- Coupons
    path('coupons/', views.coupons_list, name='coupons_list'),
    path('coupons/add', views.coupons_add, name='coupons_add'),
    path('coupons/edit/<int:coupon_pk>', views.coupons_edit, name="coupons_edit"),
    path('coupons/get_product', views.get_product, name='get_product'),
    path('coupons/delete_product/<int:coupon_pk>/', views.delete_coupon_product, name='delete_coupon_product'),

]