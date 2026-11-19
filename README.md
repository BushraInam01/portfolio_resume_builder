
# Portfolio & Resume Builder

A Django-based web application that allows users to create, customize, manage, and share professional portfolios and resumes.

Users can build their professional profiles, manage education and work experience, showcase projects and skills, connect with other users, receive skill endorsements, and download resumes as PDF files.

## Features

### Authentication
- Custom email-based user authentication
- User registration and login
- Case-insensitive email login
- Logout functionality
- Password change and password reset
- Protected user dashboards
- Secure access to user-specific resources

### Portfolio Management
- Create and manage personal portfolios
- Add and update education details
- Manage work experience
- Showcase personal and professional projects
- Add and manage technical skills
- Public portfolio with a custom URL slug
- Control portfolio visibility
- Owner-specific portfolio management

### Portfolio Customization
- Multiple resume themes:
  - Classic
  - Modern
  - Minimal
  - Professional
- Custom accent color selection
- Drag-and-drop portfolio section ordering
- Show or hide individual portfolio sections
- Section ordering and visibility reflected in public portfolios
- Section ordering and visibility reflected in resume previews and PDF exports

### Connections & Skill Endorsements
- Send and manage connection requests
- Accept, reject, cancel, and remove connections
- Discover public portfolios
- Endorse skills of accepted connections
- Prevent duplicate endorsements
- Validate connection and endorsement permissions

### Resume & PDF Export
- Resume preview
- Multiple resume templates
- Customizable resume appearance
- Download resume as PDF
- Print-friendly resume layout
- Consistent section ordering and visibility in resume output

### Portfolio Analytics
- Portfolio view counter
- Dashboard analytics
- Owner visits excluded from portfolio view counts

## Technologies Used

- Python
- Django
- Django Class-Based Views (CBVs)
- Django Templates
- Django Forms
- SQLite
- HTML5
- CSS3
- HTMX
- SortableJS
- WeasyPrint
- django-colorfield
- Pillow

## Project Structure

```text
portfolio_resume_builder/
│
├── accounts/
├── connections/
├── endorsements/
├── portfolios/
├── resumes/
├── config/
│
├── templates/
│   ├── accounts/
│   ├── portfolios/
│   ├── connections/
│   └── resumes/
│
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/BushraInam01/portfolio_resume_builder.git
```

### 2. Navigate to the Project

```bash
cd portfolio_resume_builder
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 5. Install WeasyPrint System Dependencies (Ubuntu / WSL)

WeasyPrint requires system libraries for PDF generation.

```bash
sudo apt update
sudo apt install -y libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 libharfbuzz-subset0
```

### 6. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 7. Configure Environment Variables

Set the Django environment variables before running the project.

```bash
export DJANGO_SECRET_KEY="your-secure-secret-key"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
```

Generate a secure secret key using:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 8. Apply Migrations

```bash
python3 manage.py migrate
```

### 9. Create a Superuser

```bash
python3 manage.py createsuperuser
```

### 10. Run the Development Server

```bash
python3 manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## Running Tests

Run the complete test suite:

```bash
python3 manage.py test
```

**Latest verification: 113 tests passed successfully.**

Additional project checks:

```bash
python3 manage.py check
```

Check migration consistency:

```bash
python3 manage.py makemigrations --check --dry-run
```

## Security

Security considerations implemented in this project include:

- Custom email-based authentication
- Case-insensitive email login
- Login-required access to protected views
- Portfolio ownership validation
- Owner-scoped data access
- Connection and endorsement authorization checks
- Server-side validation of section ordering and visibility
- CSRF protection
- Secure session cookie settings
- Environment-based secret key configuration
- Production-oriented HTTPS security settings

## Future Improvements

- Email notifications using SMTP
- Login rate limiting
- Production database configuration
- Deployment and hosting
- Additional portfolio themes

---

This project is developed for educational and portfolio purposes.