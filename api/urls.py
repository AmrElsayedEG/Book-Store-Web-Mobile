from django.urls import path
from api.views import (
    RegisterAPI, All_CategoriesAPI, One_CategoryProductsAPI, All_ProductsAPI, OneProductAPI, OffersAPI,
    orderAPI, CouponAPI, orderItemAPI, OneAuthorAPI, One_AuthorProductsAPI, OnePublisherAPI, One_PublisherProductsAPI,
    MyOrdersAPI, ProfileAPI, UserAPI, shippingFeesView, wishListView, forget_password, change_password,
    encodeAPI, OrderEmailAPI, feedback, CustomAuthToken, aiapi
)
from payment.views import mobile_payment_process

app_name = 'api'

urlpatterns = [
    path('user-register/', RegisterAPI.as_view()),
    path('all-categories/', All_CategoriesAPI.as_view()),
    path('category-products/', One_CategoryProductsAPI.as_view()),
    path('all-products/', All_ProductsAPI.as_view()),
    path('all-products/<int:id>/',OneProductAPI.as_view()),
    path('offers/', OffersAPI.as_view()),
    path('create-order/',orderAPI.as_view()),
    path('create-order-item/',orderItemAPI.as_view()),
    path('coupon-check/',CouponAPI.as_view()),
    path('authors/<int:id>/',OneAuthorAPI.as_view()),
    path('authors-products/',One_AuthorProductsAPI.as_view()),
    path('publishers/<int:id>/',OnePublisherAPI.as_view()),
    path('publishers-products/',One_PublisherProductsAPI.as_view()),
    path('my-orders/', MyOrdersAPI.as_view()),
    path('user-token-auth-request/',CustomAuthToken.as_view()),
    path('profile/<int:user_id>/',ProfileAPI.as_view(), name='profile-view'),
    path('user/<int:id>/', UserAPI.as_view()),
    #Shipping Fees
    path('shipping/fees/', shippingFeesView.as_view()),
    #Wishlist
    path('my-wishlist/', wishListView.as_view()),
    #Forget Password
    path('password/forget/', forget_password),
    #Change Password
    path('password/change/', change_password),
    # Recommendation
    path('product-reco/<int:id>/', aiapi),
    #PayPal
    path('encode/', encodeAPI.as_view()),
    path('payment/paypal/<sec_key>/',mobile_payment_process),
    #Order Email
    path('orderemail/', OrderEmailAPI.as_view()),
    #Feedback
    path('feedback/', feedback.as_view())
]
