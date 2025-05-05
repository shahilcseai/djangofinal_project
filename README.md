# Blood Donation Management System - Camps App

This Django application manages blood donation camps and user registrations.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Features

- Admin can create, update, and delete blood donation camps
- Users can view upcoming camps and register for them
- Admin can view registrations for each camp
- Registration is limited to one per user per camp 