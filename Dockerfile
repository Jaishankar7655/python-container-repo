# ✅ Use a lightweight and secure Python base image
FROM python:3.12-slim

# ✅ Set the working directory inside the container to /app
WORKDIR /app

# ✅ Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# ✅ Install required Python packages from requirements.txt
# --no-cache-dir avoids storing temporary installation files
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the entire Django project into the working directory
COPY . .

# ✅ Expose port 8000 to allow external access to Django's dev server
EXPOSE 8000

# ✅ Set the default command to run the Django development server
# Note: '0.0.0.0' allows access from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
