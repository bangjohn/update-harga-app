# PythonAnywhere deployment configuration

## Quick Setup Guide

### 1. Prepare Your Repository

Make sure your project is in a Git repository:

```bash
cd /home/user/update-harga-app/mysite
git init
git add .
git commit -m "Initial commit"
```

### 2. Create PythonAnywhere Account & Web App

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create an account or login
3. Go to the **Web** tab
4. Click **Add a new web app**
5. Choose **Manual configuration** (not Django template)
6. Select **Python 3.11** (or matching your version)

### 3. Set Up Virtual Environment

In PythonAnywhere's **Consoles** tab, create a bash console and run:

```bash
# Navigate to your web app directory
cd /home/yourusername

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Clone your repository (or upload files)
git clone <your-repo-url> mysite
# OR upload files manually via the Files tab

# Install dependencies
cd mysite
pip install -r requirements.txt
```

### 4. Configure Settings

Copy the production settings template:

```bash
cd /home/yourusername/mysite/mysite
cp settings_production.py settings.py
```

Edit `settings.py` and update:

```python
SECRET_KEY = 'your-random-secret-key-here'
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
CSRF_TRUSTED_ORIGINS = ['https://yourusername.pythonanywhere.com']
```

Generate a secure secret key:
```bash
python -c 'import secrets; print(secrets.token_urlsafe(50))'
```

### 5. Configure WSGI

In the **Web** tab, edit the **WSGI configuration file** and update:

```python
import os
import sys

# Add the project directory to the Python path
project_home = '/home/yourusername/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
```

### 6. Collect Static Files

In the bash console:

```bash
cd /home/yourusername/mysite
source venv/bin/activate
python manage.py collectstatic --noinput
```

### 7. Run Migrations

```bash
cd /home/yourusername/mysite
source venv/bin/activate
python manage.py migrate
```

### 8. Create Superuser (Optional)

```bash
cd /home/yourusername/mysite
source venv/bin/activate
python manage.py createsuperuser
```

### 9. Reload Web App

Go back to the **Web** tab and click **Reload** to apply changes.

### 10. Configure Media Files (if needed)

If you're using media files, ensure the `MEDIA_ROOT` path exists and is writable:

```bash
mkdir -p /home/yourusername/mysite/media
```

### 11. Test Your Site

Visit `https://yourusername.pythonanywhere.com` to see your app.

---

## Environment Variables (Optional)

For better security, use environment variables:

```bash
# In PythonAnywhere bash console
export DJANGO_SECRET_KEY='your-secret-key'
export DJANGO_ALLOWED_HOSTS='yourusername.pythonanywhere.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://yourusername.pythonanywhere.com'
```

Then update `settings.py` to read from environment variables (already done in `settings_production.py`).

---

## Troubleshooting

### 500 Error
- Check the **Error log** tab in PythonAnywhere
- Run `python manage.py check` in the console
- Ensure all dependencies are installed

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput`
- Verify `STATIC_ROOT` is set correctly
- Ensure the path exists and is accessible

### Database Issues
- SQLite database will be created at `/home/yourusername/mysite/db.sqlite3`
- Run `python manage.py migrate` to create tables

### Permission Denied
- Ensure media directory is writable: `chmod 755 /home/yourusername/mysite/media`
