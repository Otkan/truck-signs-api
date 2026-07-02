from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Category


class CategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_title = "test"
        self.test_image = "test-path"
        self.test_base_price = 0.0
        self.test_max_amount_of_lettering_items = -1
        self.test_height = 5.0
        self.test_width = 5.0

    def setUp(self):
        # Deletes all Category objects from the database to ensure a clean state before each test.
        Category.objects.all().delete()

    def test_successful_category_creation(self):
        """Tests the creation of a category."""
        category = Category.objects.create(
            title=self.test_title,
            image=self.test_image,
            base_price=self.test_base_price,
            max_amount_of_lettering_items=self.test_max_amount_of_lettering_items,
            height=self.test_height,
            width=self.test_width,
        )
        category.full_clean()
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.title, self.test_title)
        self.assertEqual(category.image, self.test_image)
        self.assertEqual(category.base_price, self.test_base_price)
        self.assertEqual(category.max_amount_of_lettering_items, self.test_max_amount_of_lettering_items)
        self.assertEqual(category.height, self.test_height)
        self.assertEqual(category.width, self.test_width)

    def test_successful_category_creation_with_default_values(self):
        """Tests that a category created with only required fields has expected default values."""
        category = Category.objects.create(title=self.test_title, image=self.test_image)
        category.full_clean()
        self.assertEqual(category.base_price, 0.0)
        self.assertEqual(category.max_amount_of_lettering_items, -1)
        self.assertEqual(category.height, 5.0)
        self.assertEqual(category.width, 5.0)

    def test_failure_category_creation_without_title(self):
        """Test the failure of category creation without a title."""
        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            category = Category(image=self.test_image)
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)

    def test_failure_category_creation_without_image_path(self):
        """Test the failure of category creation without an image-path."""
        with self.assertRaisesMessage(ValidationError, "{'image': ['This field cannot be blank.']}"):
            category = Category(title=self.test_title)
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), 0)

    def test_failure_category_creation_with_height_below_minimum(self):
        """Test that a height value below 5 raises a ValidationError."""
        with self.assertRaises(ValidationError):
            category = Category(
                title=self.test_title,
                image=self.test_image,
                height=4.9,
                width=self.test_width,
            )
            category.full_clean()
        self.assertEqual(Category.objects.count(), 0)

    def test_failure_category_creation_with_width_below_minimum(self):
        """Test that a width value below 5 raises a ValidationError."""
        with self.assertRaises(ValidationError):
            category = Category(
                title=self.test_title,
                image=self.test_image,
                height=self.test_height,
                width=0.0,
            )
            category.full_clean()
        self.assertEqual(Category.objects.count(), 0)
