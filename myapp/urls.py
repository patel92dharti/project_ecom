from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('shop/',views.shop,name='shop'),
    path('detail/<int:pk>/',views.detail,name='detail'),
    path('cart/',views.cart,name='cart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('checkout/',views.checkout,name='checkout'),
    path('billing-address/',views.billing,name='billing-address'),
    path('shipping-address/',views.shipping,name='shipping-address'),

    path('contact/',views.contact,name='contact'),
    path('seller-contact/',views.seller_contact,name='seller-contact'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('change-password',views.change_password,name='change-password'),
    path('seller-change-password',views.seller_change_password,name='seller-change-password'),
    path('profile/',views.profile,name='profile'),
    path('seller-profile/',views.seller_profile,name='seller-profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('add-product/',views.add_product,name='add-product'),
    path('view-product/',views.view_product,name='view-product'),
    path('seller-detail/<int:pk>/',views.seller_detail,name='seller-detail'),
    path('edit-seller-product/<int:pk>/',views.edit_seller_product,name='edit-seller-product'),
    path('delete-seller-product/<int:pk>/',views.delete_seller_product,name='delete-seller-product'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('change-qty/',views.change_qty,name='change-qty'),
    path('pay/', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
    
]

