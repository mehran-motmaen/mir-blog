# MirBlog App


MirBlog App
This is a blog application designed for Mir. It provides a platform to create, manage, and showcase articles along with contact forms for interaction with readers.
## Prerequisites

- Docker installed on your machine

## Running the Application and Tests

### Build the Docker Image


```bash
/mir-blog/app

sudo docker build -t mirblog-app .
```

### Run App

```bash
sudo docker run -p 8000:8000  mirblog-app
```


### Run Tests

```bash
sudo docker run --rm  mirblog-app python manage.py test

```

###  URLs

you can access the following main URLs to interact with different parts of the project:

1. **Contact Page:**
   - URL: [http://127.0.0.1:8000/blog/contact/](http://127.0.0.1:8000/blog/contact/)

2. **Articles Page:**
   - URL: [http://127.0.0.1:8000/blog/articles/](http://127.0.0.1:8000/blog/articles/)

3. **Admin Panel:**
   - URL: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - Credentials:
     - User: admin
     - Password: admin

### Email Testing

If you want to test email functionality in this project, make sure to complete the following steps in your `settings.py` file:

```python
# settings.py

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```
Replace 'your_email@gmail.com' and 'your_email_password' with your actual Gmail email address and its password. This configuration is set up for using Gmail as the SMTP server. Adjust the settings accordingly if you are using a different email provider.
### Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the StringMatcher App. Your feedback
and collaboration are appreciated.