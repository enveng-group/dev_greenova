import django
from django.conf import settings

# Initialize Django application registry
if not settings.configured:
    django.setup()

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Profile

User = get_user_model()

class UserCRUDTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.profile, _ = Profile.objects.get_or_create(user=self.user, defaults={
            'bio': '',
            'position': '',
            'department': '',
            'phone_number': '',
            'profile_image': None,
        })

    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Profile.objects.count(), 1)

    def test_user_update(self):
        """Test user update."""
        self.user.first_name = "Updated"
        self.user.save()
        self.assertEqual(User.objects.get(id=self.user.id).first_name, "Updated")

    def test_user_deletion(self):
        """Test user deletion."""
        self.user.delete()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 0)

    def test_admin_user_list_view(self):
        """Test admin user list view."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("users:admin_user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_admin_user_create_view(self):
        """Test admin user creation view."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(
            reverse("users:admin_user_create"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "Newpass123!",  # Ensure password meets validation criteria
                "password2": "Newpass123!",  # Ensure password confirmation matches
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_admin_user_edit_view(self):
        """Test admin user edit view."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(
            reverse("users:admin_user_edit", args=[self.user.id]),
            {
                "username": "updateduser",
                "email": "updateduser@example.com",
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_admin_user_delete_view(self):
        """Test admin user delete view."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("users:admin_user_delete", args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

class PasswordResetTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )

    def test_password_reset_request(self):
        """Test password reset request."""
        response = self.client.post(
            reverse("account_reset_password"),
            {"email": self.user.email},
        )
        self.assertEqual(response.status_code, 302)

    def test_password_reset_confirm(self):
        """Test password reset confirmation."""
        # Simulate password reset token generation
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.post(
            reverse("account_reset_password_from_key", args=[uid, token]),
            {
                "password1": "newpassword123",
                "password2": "newpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword123"))
