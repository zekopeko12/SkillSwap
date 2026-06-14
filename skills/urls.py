from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='skills/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/count/', views.notification_count, name='notification_count'),
    path('listings/', views.listing_list, name='listing_list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/create/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/book/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/review/', views.add_review, name='add_review'),
    path('booking/<int:booking_id>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
]