from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import ContactRequest
from blog.forms import ContactForm
from django.utils import timezone
from django.test.client import Client


class ContactRequestModelTest(TestCase):
    """
    Test cases for the ContactRequest model.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.contact_request = ContactRequest.objects.create(
            email="motmaen73@gmail.com",
            name="Test User",
            content="Test message",
        )

    def test_contact_request_creation(self):
        """
        Test the creation of a contact request instance.
        """
        self.assertEqual(
            self.contact_request.email,
            "motmaen73@gmail.com",
        )
        self.assertEqual(
            self.contact_request.name,
            "Test User",
        )
        self.assertEqual(
            self.contact_request.content,
            "Test message",
        )
        self.assertIsNotNone(self.contact_request.date)

    def test_str_representation(self):
        """
        Test the string representation of the contact request.
        """
        self.assertEqual(
            str(self.contact_request),
            "Contact Request from Test User",
        )


class ContactFormTest(TestCase):
    """
    Test cases for the ContactForm.
    """

    def test_contact_form_valid(self):
        """
        Test a valid contact form.
        """
        form_data = {
            "email": "test@example.com",
            "name": "Test User",
            "content": "Test message",
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        """
        Test an invalid contact form.
        """
        form_data = {
            "email": "invalid_email",
            "name": "",
            "content": "",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("name", form.errors)
        self.assertIn("content", form.errors)


class ContactRequestAdminTest(TestCase):
    """
    Test cases for the ContactRequest admin.
    """

    def setUp(self):
        """
        Set up the necessary data for the tests.
        """
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpassword",
            is_staff=True,
            is_superuser=True,
        )
        self.client = Client()
        self.client.login(
            username="admin",
            password="adminpassword",
        )

    def test_contact_request_admin_list_display(self):
        """
        Test the list display in the ContactRequest admin.
        """
        contact_request = ContactRequest.objects.create(
            email="test@example.com",
            name="Test User",
            content="This is a test contact request content.",
            date=timezone.now(),
        )

        response = self.client.get(reverse("admin:blog_contactrequest_changelist"))
        self.assertContains(
            response,
            "test@example.com",
        )
        self.assertContains(
            response,
            "Test User",
        )

    def test_contact_request_admin_has_add_permission(self):
        """
        Test whether the ContactRequest admin has add permission.
        """
        response = self.client.get(reverse("admin:blog_contactrequest_add"))
        self.assertEqual(
            response.status_code,
            403,
        )

    def test_contact_request_admin_has_change_permission(self):
        """
        Test whether the ContactRequest admin has change permission.
        """
        contact_request = ContactRequest.objects.create(
            email="mehran@example.com",
            name="mehran User",
            content="This is a test contact request content.",
        )

        response = self.client.get(
            reverse(
                "admin:blog_contactrequest_delete",
                args=[contact_request.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_contact_request_admin_edit_changes_object(self):
        """
        Test editing a ContactRequest object in the admin.
        """
        contact_request = ContactRequest.objects.create(
            email="mehran@example.com",
            name="mehran User",
            content="This is a test contact request content.",
        )
        updated_name = "Updated User"
        updated_content = "Updated contact request content."

        # Make a POST request to the edit page with updated data
        response = self.client.post(
            reverse(
                "admin:blog_contactrequest_change",
                args=[contact_request.id],
            ),
            {
                "email": "test@example.com",
                "name": updated_name,
                "content": updated_content,
                "date": contact_request.date,
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )


class ContactViewTest(TestCase):
    """
    Test cases for the contact view.
    """

    def test_contact_view_get(self):
        """
        Test the GET request to the contact view.
        """
        response = self.client.get(reverse("contact_form"))
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTemplateUsed(
            response,
            "contact_form.html",
        )

    def test_contact_view_post(self):
        """
        Test the POST request to the contact view.
        """
        form_data = {
            "email": "test@example.com",
            "name": "Test User",
            "content": "Test message",
        }
        response = self.client.post(
            reverse("contact_form"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTemplateUsed(
            response,
            "contact_success.html",
        )

        # Check if the contact request is saved in the database
        contact_request = ContactRequest.objects.first()
        self.assertIsNotNone(contact_request)
        self.assertEqual(
            contact_request.email,
            "test@example.com",
        )
