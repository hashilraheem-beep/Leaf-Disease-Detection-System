from django.urls import path
from LeafBack import views
from . import views

urlpatterns = [
    path('adminhome/', views.adminhome, name='adminhome'),
    path('addDisease/', views.addDisease, name='addDisease'),
    path('DiseaseSave/', views.DiseaseSave, name='DiseaseSave'),
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('Login/', views.Login, name="Login"),
    path('AdminLogout/', views.AdminLogout, name="AdminLogout"),
    path('viewdisease/', views.viewdisease, name="viewdisease"),
    path('editdisease/', views.editdisease, name="editdisease"),
    path('editdisease/', views.editdisease, name="editdisease"),
    path('updatedisease/<int:dataid>/', views.updatedisease, name="updatedisease"),
    path('UpdateDiseaseButton/<int:dataid>/', views.UpdateDiseaseButton, name="UpdateDiseaseButton"),
    path('deletedisease/<int:dataid>/', views.deletedisease, name="deletedisease"),
    path('addproduct/', views.addproduct, name="addproduct"),
    path('productsave/', views.productsave, name='productsave'),
    path('viewproduct/', views.viewproduct, name='viewproduct'),
    path('editproduct/', views.editproduct, name='editproduct'),
    path('updateproduct/<int:dataid>/', views.updateproduct, name="updateproduct"),
    path('UpdateProductButton/<int:dataid>/', views.UpdateProductButton, name="UpdateProductButton"),
    path('deleteproduct/<int:dataid>/', views.deleteproduct, name="deleteproduct"),
    path('users', views.users, name="users"),
    path('deleteuser/<int:dataid>/', views.deleteuser, name="deleteuser"),
    path('adduser', views.adduser, name="adduser"),
    path('order/', views.order, name="order"),
    path('user_orders_detail/<str:username>/', views.user_orders_detail, name="user_orders_detail"),
    path('deleteorder/<int:dataid>/', views.deleteorder, name="deleteorder"),
    path('send-order-confirmation/', views.send_order_confirmation, name='send_order_confirmation'),
    path('delete-all-user-orders/<str:username>/', views.delete_all_user_orders, name='delete_all_user_orders'),
]
