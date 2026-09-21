from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Laptop',
            slug='test-laptop',
            price=1000.00,
            stock=2,
        )
    
    def test_product_str(self):
        self.assertTrue(str(self.product), 'Test Laptop')
        
    def test_in_stock_true_when_stock_positive(self):
        self.assertTrue(self.product.in_stock())

    def test_in_stock_false_when_zero(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.in_stock())

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Electronics')
