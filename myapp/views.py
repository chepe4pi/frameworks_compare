from django.db import connection
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


def get_order(self, order_id, *args, **kwargs):
    with connection.cursor() as cursor:
        # Get order and related customer information using raw SQL
        cursor.execute("""
            SELECT o.id, o.created_at, c.id as customer_id, c.name as customer_name, c.email as customer_email
            FROM myapp_order o
            JOIN myapp_customer c ON o.customer_id = c.id
            WHERE o.id = %s
        """, [order_id])
        order_row = cursor.fetchone()

        if not order_row:
            return JsonResponse({'error': 'Order not found'}, status=404)

        order_instance = {
            'id': order_row[0],
            'created_at': order_row[1],
            'customer': {
                'id': order_row[2],
                'name': order_row[3],
                'email': order_row[4]
            }
        }

        # Get products related to the order using raw SQL
        cursor.execute("""
            SELECT p.id, p.name, p.price
            FROM myapp_product p
            JOIN myapp_order_products op ON p.id = op.product_id
            WHERE op.order_id = %s
        """, [order_id])
        product_rows = cursor.fetchall()

        product_data = [
            {'id': row[0], 'name': row[1], 'price': row[2]} for row in product_rows
        ]

    combined_data = {
        'order': order_instance,
        'products': product_data,
    }

    return JsonResponse(combined_data)
