# Python image as the base image
FROM python:3.11.3

# Setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Installing dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the Django application into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application's port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "seshbookmark.wsgi:application"]
