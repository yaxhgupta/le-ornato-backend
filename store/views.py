from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.db.models import Sum

from .models import Product, Category, Order, Banner   # <-- Added Order here
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, BannerSerializer  # <-- Added both here



# -------------------- PRODUCTS --------------------
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        product = serializer.save()
        product.recalculate_price()


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
    })


# -------------------- ADMIN DASHBOARD --------------------
class RecentOrdersView(APIView):
    def get(self, request):
        orders = Order.objects.order_by("-created_at")[:5]
        return Response(OrderSerializer(orders, many=True).data)

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


class LowStockProductsView(APIView):
    def get(self, request):
        low_stock = Product.objects.filter(stock__lte=3)
        return Response(ProductSerializer(low_stock, many=True).data)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AdminStatsView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(stock__lte=3).count()
        total_orders = Order.objects.count()
        total_sales = Order.objects.aggregate(Sum("total_amount"))["total_amount__sum"] or 0
        total_customers = Order.objects.values("customer").distinct().count()

        return Response({
            "total_products": total_products,
            "low_stock_count": low_stock_count,
            "total_orders": total_orders,
            "total_sales": total_sales,
            "total_customers": total_customers,
        })


class ReportListView(APIView):
    def get(self, request):
        sales_by_category = (
            Order.objects.values("items__product__category__name")
            .annotate(total_sales=Sum("items__product__price"))
            .order_by("-total_sales")
        )
        return Response(list(sales_by_category))

class BannerListView(generics.ListCreateAPIView):  # You can also allow creating new banners
    queryset = Banner.objects.all().order_by('-id')
    serializer_class = BannerSerializer
