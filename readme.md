# python 3.9.6

# Django + Nginx + Gunicorn Setup Guide

This guide provides an overview of setting up a Django application with Nginx and Gunicorn, including using virtual environments, managing dependencies, and deploying in a production environment.

## 1. Setting Up a Python Virtual Environment
A virtual environment allows you to manage dependencies for your project independently, avoiding conflicts between different projects.

### Create a Virtual Environment
- Use Python's `venv` module to create a virtual environment:
  ```bash
  python3 -m venv venv
  ```
  This creates a `venv` directory containing the virtual environment.

### Activate the Virtual Environment
- **Linux / macOS**:
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

### Deactivate the Virtual Environment
- To deactivate the virtual environment and return to the system Python:
  ```bash
  deactivate
  ```

## 2. Managing Dependencies with `requirements.txt`
`requirements.txt` is used to record the Python packages required for your project.

### Export Dependencies to `requirements.txt`
- To export the list of currently installed packages to `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```
  This creates a file that lists all installed packages and their versions, such as:
  ```
  Django==3.2.9
  djangorestframework==3.12.4
  gunicorn==20.1.0
  ```

### Install Dependencies from `requirements.txt`
- To install all required packages from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## 3. Running Django in Development
To run the Django development server, use the following command:

```bash
python manage.py runserver
```
- This runs the server on `127.0.0.1:8000` by default. You can specify a different port like this:
  ```bash
  python manage.py runserver 8080
  ```
- For external access, you can bind to all IP addresses:
  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```

## 4. Deploying Django with Gunicorn and Nginx
In a production environment, Django should be served using a WSGI server like **Gunicorn** along with a reverse proxy like **Nginx**.

### Install Gunicorn
- Install Gunicorn in your virtual environment:
  ```bash
  pip install gunicorn
  ```

### Run Django with Gunicorn
- Use Gunicorn to run the Django application:
  ```bash
  gunicorn myproject.wsgi:application
  ```
  - Replace `myproject` with your Django project name.

### Running with Unix Socket for Nginx
- To connect Gunicorn and Nginx via a Unix socket:
  ```bash
  gunicorn myproject.wsgi:application --bind unix:/home/kaist-220v/myproject/gunicorn.sock
  ```
- To run Gunicorn in the background (useful for production):
  ```bash
  gunicorn myproject.wsgi:application --bind unix:/home/kaist-220v/myproject/gunicorn.sock --daemon
  ```

### Nginx Configuration
- Configure Nginx to serve static files and proxy requests to Gunicorn.

  **Example Nginx Configuration**:
  ```nginx
  server {
      listen 80;
      server_name example.com;

      # Frontend (React build files) handling
      root /home/kaist-220v/project-solar-see-frontend/build;
      index index.html;

      location / {
          try_files $uri $uri/ /index.html;
      }

      # Backend (Django) requests handling
      location /api/ {
          include proxy_params;
          proxy_pass http://unix:/home/kaist-220v/project-solar-see-backend/gunicorn.sock;
      }
  }
  ```
- This configuration sets up Nginx to serve both static files for the frontend and proxy backend API requests to Gunicorn.

## 5. Managing Gunicorn with Supervisor (Optional)
For production environments, it is common to use **Supervisor** to manage Gunicorn and ensure it restarts if it crashes.

### Install Supervisor
```bash
sudo apt install supervisor
```

### Supervisor Configuration for Gunicorn
Create a Supervisor configuration file for Gunicorn:

```ini
[program:gunicorn]
directory=/home/kaist-220v/myproject
command=/home/kaist-220v/myproject/venv/bin/gunicorn myproject.wsgi:application --bind unix:/home/kaist-220v/myproject/gunicorn.sock
autostart=true
autorestart=true
stderr_logfile=/var/log/gunicorn.err.log
stdout_logfile=/var/log/gunicorn.out.log
```

Update and start the Supervisor service:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start gunicorn
```

## Summary
This guide helps you set up a Django project in both development and production environments using **virtual environments**, **Gunicorn**, and **Nginx**. Using these tools ensures better performance, stability, and security for your project.

