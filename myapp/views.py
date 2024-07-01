from asgiref.sync import sync_to_async
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Order, Product
from .serializers import OrderSerializer, ProductSerializer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):

        order_id = kwargs.get('pk')
        order_instance = self.get_object()
        order_serialized = OrderSerializer(order_instance).data

        products_queryset = Product.objects.filter(orders__in=[order_id])
        products_serialized = ProductSerializer(products_queryset, many=True).data

        combined_data = {
            "order": order_serialized,
            "products": products_serialized,
        }

        return Response(combined_data)
