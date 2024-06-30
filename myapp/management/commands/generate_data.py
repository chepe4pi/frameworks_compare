# myapp/management/commands/generate_data.py

import asyncio
from aiomultiprocess import Pool
from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker
import random
import time
from asgiref.sync import sync_to_async

import django
from django.db.models import Max, Min

django.setup()


class Command(BaseCommand):
    help = 'Generate random data for Customer, Product and Order models'

    def handle(self, *args, **kwargs):
        start_time = time.time()
        for i in range(1000):
            asyncio.run(self.generate_data())
        end_time = time.time()
        self.stdout.write(self.style.SUCCESS(f'Data generation completed in {end_time - start_time} seconds'))

    async def generate_customers(self, num_customers):
        Customer = apps.get_model('myapp', 'Customer')
        async with Pool() as pool:
            await pool.map(self.create_customer, [(i, Customer) for i in range(num_customers)])

    async def generate_products(self, num_products):
        Product = apps.get_model('myapp', 'Product')
        async with Pool() as pool:
            await pool.map(self.create_product, [(i, Product) for i in range(num_products)])

    async def generate_orders(self, num_orders):
        Product = apps.get_model('myapp', 'Product')
        Customer = apps.get_model('myapp', 'Customer')
        Order = apps.get_model('myapp', 'Order')

        async with Pool() as pool:
            await pool.map(self.create_order, [(i, Customer, Product, Order) for i in range(num_orders)])

    async def generate_data(self):
        # Create customers and products first to get their IDs
        num_products = 50
        num_customers = 100
        num_orders = 1000

        await self.generate_customers(num_customers)
        await self.generate_products(num_products)
        await self.generate_orders(num_orders)

    @staticmethod
    async def create_customer(args):
        _, Customer = args
        await sync_to_async(Customer.objects.create)(
            email=Faker().email(),
            name=Faker().name()
        )

    @staticmethod
    async def create_product(args):
        _, Product = args
        await sync_to_async(Product.objects.create)(
            name=Faker().word(),
            price=Faker().pydecimal(left_digits=5, right_digits=2, positive=True)
        )

    @staticmethod
    async def create_order(args):
        _, Customer, Product, Order = args
        customer_last_id = await sync_to_async(Customer.objects.aggregate)(Max('id'))
        product_last_id = await sync_to_async(Product.objects.aggregate)(Max('id'))

        customer_first_id = await sync_to_async(Customer.objects.aggregate)(Min('id'))
        product_first_id = await sync_to_async(Product.objects.aggregate)(Min('id'))

        customer = await sync_to_async(Customer.objects.get)(id=random.randint(customer_first_id['id__min'], customer_last_id['id__max']))
        order = await sync_to_async(Order.objects.create)(customer=customer)
        products_ids = []
        for _ in range(random.randint(1, 5)):
            product_id = await sync_to_async(Product.objects.get)(id=random.randint(product_first_id['id__min'], product_last_id['id__max']))
            products_ids.append(product_id)
        await sync_to_async(order.products.set)(products_ids)