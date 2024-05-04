from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('checkout/', checkout, name='checkout'),

    # Cart
	path('cart/', view_cart, name='view_cart'),
	path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    
    # wishlist
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:item_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    # Authentication part
    path('register/',register,name='register'),
    path('login/',log_in,name='login'),
    path('logout/',log_out,name='logout'),
    path('change_password',change_password, name='change_password'),

    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/login.html'), name='password_reset_complete'),

    # Cetegories
    path('product/<int:pk>', product, name='product'),
    path('category/<str:space>', category, name='category'),
    path('category_summary/', category_summary, name='category_summary'),

]

