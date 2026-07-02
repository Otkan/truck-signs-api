from django.urls import re_path

# from .views import PricesPageAPI,HowToAPIView, CreateOrderAPI, OrderSummaryAPIView, RetrieveAllProductColorsAPI
from .views import (
    CategoryListView,
    CommentCreateView,
    CommentsView,
    CreateOrder,
    LetteringItemCategoryListView,
    LogoListView,
    PaymentView,
    ProductColorListView,
    ProductDetail,
    ProductFromCategoryListView,
    ProductListView,
    ProductVariationRetrieveView,
    RetrieveOrder,
    UploadCustomerImage,
)

app_name = "tsa_products"

urlpatterns = [
    re_path(r"^categories/$", CategoryListView.as_view(), name="categories-api"),
    re_path(
        r"^lettering-item-categories/$", LetteringItemCategoryListView.as_view(), name="lettering-item-categories-api"
    ),
    re_path(r"^products/$", ProductListView.as_view(), name="products-api"),
    re_path(r"^product-category/(?P<id>[0-9]+)/$", ProductFromCategoryListView.as_view(), name="product-category-api"),
    re_path(
        r"^product-variation-retrieve/(?P<id>[0-9]+)/$",
        ProductVariationRetrieveView.as_view(),
        name="product-category-api",
    ),
    re_path(r"^product-color/$", ProductColorListView.as_view(), name="product-color-api"),
    re_path(r"^product-detail/(?P<id>[0-9]+)/$", ProductDetail.as_view(), name="product-detail-api"),
    re_path(r"^truck-logo-list/$", LogoListView.as_view(), name="truck-logo-list-api"),
    re_path(r"^order/(?P<id>[0-9]+)/create/$", CreateOrder.as_view(), name="create-order-api"),
    re_path(r"^order/(?P<id>[0-9]+)/retrieve/$", RetrieveOrder.as_view(), name="retrieve-order-api"),
    re_path(r"^order-payment/(?P<id>[0-9]+)/$", PaymentView.as_view(), name="order-payment-api"),
    re_path(r"^comments/$", CommentsView.as_view(), name="comments-api"),
    re_path(r"^comment/create/$", CommentCreateView.as_view(), name="comment-create-api"),
    re_path(r"^upload-customer-image/$", UploadCustomerImage.as_view(), name="upload-customer-image-api"),
]
