# # myapp/factories.py
#
# import factory
# from django.apps import apps
# from factory.django import DjangoModelFactory
#
# # Product = apps.get_model('myapp', 'Product')
# # Customer = apps.get_model('myapp', 'Customer')
# # Order = apps.get_model('myapp', 'Order')
#
#
# class CustomerFactory(DjangoModelFactory):
#     class Meta:
#         model = apps.get_model('myapp', 'Customer')
#
#     name = factory.Faker('name')
#     email = factory.Faker('email')
#
#
# class ProductFactory(DjangoModelFactory):
#     class Meta:
#         model = apps.get_model('myapp', 'Product')
#
#     name = factory.Faker('word')
#     price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
#
#
# class OrderFactory(DjangoModelFactory):
#     class Meta:
#         model = apps.get_model('myapp', 'Order')
#
#     customer = factory.SubFactory(CustomerFactory)
