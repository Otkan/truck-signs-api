from django.core.exceptions import ValidationError
from django.test import TestCase

from tsa_products.models import Comment


class CommentTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user_email = "test-email"
        self.test_image = "test-path"
        self.test_text = "test-text"
        self.test_visible = False

    def setUp(self):
        # Deletes all Comment objects from the database to ensure a clean state before each test.
        Comment.objects.all().delete()

    def test_successful_comment_creation(self):
        """Tests the creation of a comment."""
        comment = Comment.objects.create(
            user_email=self.test_user_email, image=self.test_image, text=self.test_text, visible=self.test_visible
        )
        comment.full_clean()
        created_comment = Comment.objects.first()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertIsNotNone(created_comment)
        self.assertEqual(created_comment.user_email, self.test_user_email)
        self.assertEqual(created_comment.image, self.test_image)
        self.assertEqual(created_comment.text, self.test_text)
        self.assertEqual(created_comment.visible, self.test_visible)

    def test_failure_comment_creation_without_user_email(self):
        """Test the failure of comment creation without a user mail address."""
        with self.assertRaisesMessage(ValidationError, "{'user_email': ['This field cannot be blank.']}"):
            comment = Comment(image=self.test_image)
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)

    def test_successful_comment_creation_with_default_values(self):
        """Tests that a comment created with only required fields has expected default values."""
        comment = Comment.objects.create(user_email=self.test_user_email, image=self.test_image)
        comment.full_clean()
        self.assertEqual(comment.text, "")
        self.assertFalse(comment.visible)

    def test_failure_comment_creation_without_image(self):
        """Test the failure of comment creation without an image-path."""
        with self.assertRaisesMessage(ValidationError, "{'image': ['This field cannot be blank.']}"):
            comment = Comment(user_email=self.test_user_email)
            comment.full_clean()
            comment.save()
        self.assertEqual(Comment.objects.count(), 0)
