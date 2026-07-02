from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import LetteringItemCategory


class LetteringItemCategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_title = "test"
        self.test_price = 0.0

    def setUp(self):
        # Deletes all LetteringItemCategory objects from the database to ensure a clean state before each test.
        LetteringItemCategory.objects.all().delete()

    def test_successful_lettering_item_category_creation(self):
        """Tests the creation of a lettering item category."""
        lettering_item_category = LetteringItemCategory.objects.create(title=self.test_title, price=self.test_price)
        lettering_item_category.full_clean()
        self.assertEqual(LetteringItemCategory.objects.count(), 1)
        self.assertEqual(lettering_item_category.title, self.test_title)
        self.assertEqual(lettering_item_category.price, self.test_price)

    def test_successful_lettering_item_category_creation_with_default_price(self):
        """Tests that a lettering item category created without a price has the expected default price."""
        lettering_item_category = LetteringItemCategory.objects.create(title=self.test_title)
        lettering_item_category.full_clean()
        self.assertEqual(lettering_item_category.price, 0.0)

    def test_failure_lettering_category_creation_without_title(self):
        """Test the failure of lettering item category creation without a title."""
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            lettering_item_category = LetteringItemCategory(price=self.test_price)
            lettering_item_category.full_clean()
            lettering_item_category.save()
        self.assertEqual(LetteringItemCategory.objects.count(), 0)
