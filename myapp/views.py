from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().select_related('customer').prefetch_related('products')
    serializer_class = OrderSerializer
