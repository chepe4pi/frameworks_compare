import asyncio

from django.http import JsonResponse
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


async def get_order(self, order_id, *args, **kwargs):

    async def get_order_instance(order_id):
        order_instance = await Order.objects.select_related('customer').aget(id=order_id)
        return order_instance

    async def get_products(order_id):
        product_data = []
        async for product in Product.objects.filter(orders__in=[order_id]):
            product_data.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
            })
        return product_data

    order_instance, product_data = await asyncio.gather(
        get_order_instance(order_id),
        get_products(order_id),
    )

    combined_data = {
        "order": {
            "id": order_instance.id,
            "customer": {
                "id": order_instance.customer.id,
                "name": order_instance.customer.name,
                "email": order_instance.customer.email,
            },
            "created_at": order_instance.created_at,
        },
        "products": product_data,
    }

    return JsonResponse(combined_data)
