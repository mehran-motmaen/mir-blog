FROM python:3.13.0a2-alpine3.18

LABEL maintainer="Merhan Motmaen <motmaen73@gmail.com>"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set an environment variable for the application name
ENV APP_NAME=MirBlogApp

# Expose the port that the application will run on
EXPOSE 8000

# Run the Django development server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]