from django.urls import path,include
from . import views
from .views import redirect_based_on_usertype

urlpatterns = [
    path('', views.home , name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('redirect/', redirect_based_on_usertype, name='redirect_based_on_usertype'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('hospital_dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('dispensary_dashboard/', views.dispensary_dashboard, name='dispensary_dashboard'),
    path('manufacturer_dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),
    path('product_list/', views.product_list, name='product_list'),
    path('book/', views.book_product, name='book_product'),
    path('success/', views.success_page, name='success_page'),
    path('add-product/', views.add_product, name='add_product'),
]
