"""restaurants_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from res_cus import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomUserView.as_view(), name='signup'),
    path('myprofile/', TemplateView.as_view(template_name='myprofile.html'), name='myprofile'),
    path('edit/<slug:slug>/', views.EditProfile, name='editprofile'),
    path('delete/<slug:slug>/', views.DeleteProfile, name='deleteprofile'),
    path('addrestaurant/<slug:slug>/', views.AddRestaurant, name='addrestaurant'),
    path('managerestaurants/<slug:slug>/', views.ManageRestaurants, name='managerestaurants'),
    path('editrestaurant/<slug:slug>/<int:pk>/', views.EditRestaurant, name='editrestaurant'),
    path('deleterestaurant/<slug:slug>/<int:pk>/', views.DeleteRestaurant, name='deleterestaurant'),
    path('deleteimgrestaurant/<slug:slug>/<int:pk>/', views.DeleteImgRestaurant, name='deleteimgrestaurant'),
    path('listrestaurants/', views.ListRestaurants, name='listrestaurants'),
    path('restaurant/<int:pk>/', views.ViewRestaurant, name='viewrestaurant'),
    path('likes/', views.LikeRestaurant, name='like_restaurant'),
    path('likes/<int:pk>/', views.LikeRestaurantFromRestaurant, name='like_restaurant_from_restaurant'),
    path('restaurant/<int:pk>/addfood/', views.AddFood, name='addfood'),
    path('restaurant/<int:pk1>/<int:pk2>/editfood/', views.EditFood, name='editfood'),
    path('restaurant/<int:pk1>/<int:pk2>/deletefood/', views.DeleteFood, name='deletefood'),
    path('restaurant/<int:pk>/deleteimgfood/', views.DelteImgFood, name='deleteimgfood'),
    path('food/<int:pk>/', views.ViewFood, name='viewfood'),
    path('ratingfood/<int:pk>/', views.RatingFood, name='ratingfood')


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)