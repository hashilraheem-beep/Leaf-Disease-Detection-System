from django.urls import path
from LeafFront import views

urlpatterns = [
    path('home/', views.home, name='home'),             
    path('predictresult/', views.predictresult, name='predictresult'),
    path('about/', views.about, name='about'),
    path('indexabout/', views.indexabout, name='indexabout'),
    path('shop/', views.shop, name='shop'),
    path('', views.index, name='index'),
    path('productmore/<int:dataid>/', views.productmore, name='productmore'),
    path('signup/', views.signup, name='signup'),
    path('createaccount/', views.createaccount, name='createaccount'),        
    path('login/', views.login, name='login'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('logout/', views.logout, name="logout"),
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('cart/', views.cart, name="cart"),
    path('remove_cart/<int:id>/', views.remove_cart, name='remove_cart'),
    path('update_cart/<int:id>/', views.update_cart, name='update_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('confirmorder', views.confirmorder, name='confirmorder'),
    path('diseaseinfo/', views.diseaseinfo, name='diseaseinfo'),
]
