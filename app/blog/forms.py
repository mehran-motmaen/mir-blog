from django import forms


class ContactForm(forms.Form):
    """
    A Django form for handling contact information.

    Fields:
    - email (EmailField): The email address of the person making the contact request.
    - name (CharField): The name of the person making the contact request (maximum length: 255 characters).
    - content (CharField): The content or message of the contact request.

    Widgets:
    - email: EmailInput
    - name: TextInput
    - content: Textarea
    """

    email = forms.EmailField(
        label='Your Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    name = forms.CharField(
        max_length=255,
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label='Your Message',
    )
