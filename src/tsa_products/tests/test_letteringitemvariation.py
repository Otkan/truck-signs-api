from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category, LetteringItemCategory, LetteringItemVariation, Product, ProductVariation


class LetteringItemVariationTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_lettering_item_category = LetteringItemCategory.objects.create(title="test")
        self.test_lettering = "test"
        self.test_product_variation = ProductVariation.objects.create(
            product=Product.objects.create(
                category=Category.objects.create(title="test", image="test-path"), title="test-title"
            )
        )

    def setUp(self):
        # Deletes all LetteringItemVariation objects from the database to ensure a clean state before each test.
        LetteringItemVariation.objects.all().delete()

    def test_successful_lettering_item_variation_creation(self):
        """Tests the creation of a lettering item variation."""
        lettering_item_variation = LetteringItemVariation.objects.create(
            lettering_item_category=self.test_lettering_item_category,
            lettering=self.test_lettering,
            product_variation=self.test_product_variation,
        )
        lettering_item_variation.full_clean()
        self.assertEqual(LetteringItemVariation.objects.count(), 1)
        self.assertEqual(lettering_item_variation.lettering, self.test_lettering)
        self.assertEqual(lettering_item_variation.lettering_item_category, self.test_lettering_item_category)
        self.assertEqual(lettering_item_variation.product_variation, self.test_product_variation)

    def test_failure_lettering_item_variation_creation_without_lettering(self):
        """Test the failure of lettering item variation creation without a lettering."""
        with self.assertRaisesMessage(ValidationError, "{'lettering': ['This field cannot be blank.']}"):
            lettering_item_variation = LetteringItemVariation(product_variation=self.test_product_variation)
            lettering_item_variation.full_clean()
            lettering_item_variation.save()
        self.assertEqual(LetteringItemVariation.objects.count(), 0)
