from .register import RegisterAPI
from .category import All_CategoriesAPI, One_CategoryProductsAPI
from .products import All_ProductsAPI, OneProductAPI
from .offers import OffersAPI
from .order import orderAPI, orderItemAPI
from .coupon import CouponAPI
from .author import OneAuthorAPI, One_AuthorProductsAPI
from .publisher import OnePublisherAPI, One_PublisherProductsAPI
from .my_orders import MyOrdersAPI
from .profile import ProfileAPI, UserAPI
from .shipping_fees import shippingFeesView
from .wishlist import wishListView
from .password import forget_password, change_password
from .encode import encodeAPI
from .order_email import OrderEmailAPI
from .feedback import feedback
from .login import CustomAuthToken
from .recommendation import aiapi