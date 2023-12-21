from django import forms
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    """
    A Django Form for handling contact requests.

    Model:
    - ContactRequest: Model for storing contact requests.

    Fields:
    - email (EmailField): The email address of the person making the contact request.
    - name (CharField): The name of the person making the contact request (maximum length: 255 characters).
    - content (CharField): The content or message of the contact request.

    Widgets:
    - email: EmailInput
    - name: TextInput
    - content: Textarea
    """

    class Meta:
        model = ContactRequest
        fields = [
            "email",
            "name",
            "content",
        ]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }
