from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tsa_products.models import Category, Order, Product, ProductVariation


class OrderTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_ordered_date = timezone.now()
        self.test_user_email = "test-email"
        self.test_user_first_name = "test-name"
        self.test_user_last_name = "test-surname"
        self.test_address1 = "Address line 1"
        self.test_address2 = "Address line 2"
        self.test_ordered = False
        self.test_product = ProductVariation.objects.create(
            product=Product.objects.create(
                category=Category.objects.create(title="test", image="test-path"), title="test-title"
            )
        )
        self.test_comment = "test-comment"

    def setUp(self):
        # Deletes all Order objects from the database to ensure a clean state before each test.
        Order.objects.all().delete()

    def test_successful_order_creation(self):
        """Tests the creation of an order."""
        order = Order.objects.create(
            ordered_date=self.test_ordered_date,
            user_email=self.test_user_email,
            user_first_name=self.test_user_first_name,
            user_last_name=self.test_user_last_name,
            address1=self.test_address1,
            address2=self.test_address2,
            ordered=self.test_ordered,
            product=self.test_product,
            comment=self.test_comment,
        )
        order.full_clean()
        self.assertEqual(Order.objects.count(), 1)
        self.assertIsNotNone(order.ordered_date)
        self.assertEqual(order.user_email, self.test_user_email)
        self.assertEqual(order.user_first_name, self.test_user_first_name)
        self.assertEqual(order.user_last_name, self.test_user_last_name)
        self.assertEqual(order.address1, self.test_address1)
        self.assertEqual(order.address2, self.test_address2)
        self.assertEqual(order.ordered, self.test_ordered)
        self.assertEqual(order.product, self.test_product)
        self.assertEqual(order.comment, self.test_comment)

    def test_successful_order_creation_with_default_values(self):
        """Tests that an order created with only the required user_email field has expected default values."""
        order = Order.objects.create(user_email=self.test_user_email)
        order.full_clean()
        self.assertIsNotNone(order.ordered_date)
        self.assertFalse(order.ordered)
        self.assertEqual(order.address1, "Address line 1")
        self.assertEqual(order.address2, "Address line 2")
        self.assertEqual(order.comment, "")

    def test_failure_order_creation_without_user_email(self):
        """Test the failure of order creation without a user_email."""
        with self.assertRaisesMessage(ValidationError, "{'user_email': ['This field cannot be blank.']}"):
            order = Order(user_first_name=self.test_user_first_name)
            order.full_clean()
            order.save()
        self.assertEqual(Order.objects.count(), 0)
