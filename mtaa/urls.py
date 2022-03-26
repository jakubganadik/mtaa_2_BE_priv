"""mtaa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

import mtaa_main

urlpatterns = [
    path('RegisterUser/', mtaa_main.user_reg),
    path('LoginUser/', mtaa_main.user_log),
    path('RegisterRestaurant/', mtaa_main.rest_insert),
    path('GetRestaurantList/', mtaa_main.rest_list),
    path('GetRestaurantDetail/<int:rest_id>', mtaa_main.rest_det),
    path('CreateBooking/', mtaa_main.book_create),
    path('EditBooking/<int:book_id>', mtaa_main.book_edit),
    path('DeleteBooking/<int:book_id>', mtaa_main.book_del),
    path('GetBookings/<int:user_id>', mtaa_main.book_get),
    path('GetBookingDetail/<int:book_id>', mtaa_main.book_det),
    path('DeleteAllPastBookings/', mtaa_main.book_delall)

]
