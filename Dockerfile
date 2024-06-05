# Use an official Python runtime as a parent image
FROM python:3.10-slim

# setting the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=social_network.settings

# Run the Django development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Apply Migrations and run the Django Server

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]