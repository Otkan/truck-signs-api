from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category, Product


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_category = Category.objects.create(title="test", image="test-path")
        self.test_title = "test-title"
        self.test_image = "test-path"
        self.test_detail_image = "test-detail-path"
        self.test_is_uploaded = False

    def setUp(self):
        # Deletes all Product objects from the database to ensure a clean state before each test.
        Product.objects.all().delete()

    def test_successful_product_creation(self):
        """Tests the creation of a product."""
        product = Product.objects.create(
            category=self.test_category,
            title=self.test_title,
            image=self.test_image,
            detail_image=self.test_detail_image,
            is_uploaded=self.test_is_uploaded,
        )
        product.full_clean()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.category, self.test_category)
        self.assertEqual(product.title, self.test_title)
        self.assertEqual(product.image, self.test_image)
        self.assertEqual(product.detail_image, self.test_detail_image)
        self.assertEqual(product.is_uploaded, self.test_is_uploaded)

    def test_successful_product_creation_with_default_values(self):
        """Tests that a product created with only required fields has expected default values."""
        product = Product.objects.create(category=self.test_category, title=self.test_title)
        product.full_clean()
        self.assertFalse(product.is_uploaded)
        self.assertEqual(product.image, "")
        self.assertEqual(product.detail_image, "")

    def test_failure_product_creation_without_category(self):
        """Test the failure of product creation without a category."""
        with self.assertRaisesMessage(ValidationError, "{'category': ['This field cannot be null.']}"):
            product = Product(title=self.test_title)
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)

    def test_failure_product_creation_without_title(self):
        """Test the failure of product creation without a title."""
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            product = Product(category=self.test_category)
            product.full_clean()
            product.save()
        self.assertEqual(Product.objects.count(), 0)
