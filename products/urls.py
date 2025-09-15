from django.urls import path

from products.views import GetProductsAPIView, GetCategoryAPIView

app_name = 'products'

urlpatterns = [
    path("products/", GetProductsAPIView.as_view(), name='get-product'),
    path("products/<int:pk>/", GetProductsAPIView.as_view()),
    # path("p/",GetPaginate.as_view()),
    path('categories/',GetCategoryAPIView.as_view()),
    path('categories/<int:pk>/', GetCategoryAPIView.as_view()),
]




