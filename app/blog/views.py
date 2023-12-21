from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import Article
from .forms import ContactForm
from app import settings
from threading import Thread


class ArticleListView(ListView):
    """
    View for displaying a list of articles.

    Attributes:
    - model (Article): The model used for retrieving the list of articles.
    - template_name (str): The name of the template to be rendered.
    - context_object_name (str): The name of the variable to use in the template for the list of articles.
    - paginate_by (int): The number of articles to display per page.
    """

    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        """
        Override the queryset to include only online articles.
        """

        return self.model.objects.filter(is_online=True)


class ArticleDetailView(DetailView):
    """
    View for displaying the details of a single article.

    Attributes:
    - model (Article): The model used for retrieving the article details.
    - template_name (str): The name of the template to be rendered.
    - context_object_name (str): The name of the variable to use in the template for the article object.
    """

    model = Article
    template_name = "article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        """
        Override the queryset to include only online articles.
        """
        return self.model.objects.filter(is_online=True)


class ContactView(FormView):
    """
    A view for handling contact form submissions and sending emails asynchronously.
    """

    template_name = "contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success.html")

    @staticmethod
    def send_contact_email(name, email, content):
        """
        Sends a contact email in a separate thread.

        Parameters:
        - name (str): The name of the person making the contact request.
        - email (str): The email address of the person making the contact request.
        - content (str): The content or message of the contact request.

        Returns:
        None
        """
        # Email subject
        subject = "New Contact Request"

        # Email message body with name, email, and content
        message = f"Name: {name}\n Reply-To: {email}\nContent: {content}"

        try:
            # Send email using Django's send_mail function
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=settings.RECIPIENT_EMAIL,
                fail_silently=False,
            )
        except Exception as e:
            # todo
            #  Handle exceptions based on your requirements
            print(f"Error sending email: {e}")

    def send_contact_email_threaded(self, sender_name, sender_email, message_content):
        """
        Sends a contact email in a separate thread.

        Parameters:
        - sender_name (str): The name of the person making the contact request.
        - sender_email (str): The email address of the person making the contact request.
        - message_content (str): The content or message of the contact request.

        Returns:
        None
        """
        thread = Thread(
            target=self.send_contact_email,
            args=(sender_name, sender_email, message_content),
        )
        thread.start()

    def form_valid(self, form):
        """
        Handles a valid form submission.

        Saves the contact request to the database and sends a contact email in a separate thread.

        Parameters:
        - form (ContactForm): The validated contact form.

        Returns:
        HttpResponse: The HTTP response for the successful form submission.
        """
        # Save contact request to the database
        contact_request = form.save()

        # Send contact email in a separate thread
        self.send_contact_email_threaded(
            contact_request.name,
            contact_request.email,
            contact_request.content,
        )
        return super().form_valid(form)
