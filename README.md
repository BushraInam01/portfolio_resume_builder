# Portfolio & Resume Builder

A Django-based web application that allows users to create, customize, manage, and share professional portfolios and resumes.

Users can build their professional profiles, manage education and work experience, showcase projects and skills, connect with other users, receive skill endorsements, and download resumes as PDF files.

## Features

### Authentication
- Custom email-based user authentication
- User registration and login
- Logout functionality
- Password change and password reset
- Protected user dashboards

### Portfolio Management
- Create and manage personal portfolios
- Add and update education details
- Manage work experience
- Showcase personal and professional projects
- Add and manage technical skills
- Public portfolio with a custom slug
- Control portfolio visibility

### Portfolio Customization
- Multiple resume themes:
  - Classic
  - Modern
  - Minimal
  - Professional
- Custom accent color selection
- Drag-and-drop portfolio section ordering
- Show or hide portfolio sections (applied to the public portfolio and the resume)

### Connections & Skill Endorsements
- Send and manage connection requests
- Accept, reject, cancel, and remove connections
- Discover public portfolios
- Endorse skills of accepted connections
- Prevent duplicate endorsements

### Resume & PDF Export
- Resume preview
- Multiple resume templates
- Customizable resume appearance
- Download resume as PDF
- Print-friendly resume layout

### Portfolio Analytics
- Portfolio view counter
- Dashboard analytics

## Technologies Used

- Python
- Django
- Django Class-Based Views (CBVs)
- Django Templates
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

### 5. Install System Libraries (needed by WeasyPrint)

PDF export needs the Pango library on your system. Without it,
`import weasyprint` fails.

- **Ubuntu / Debian:** `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`
- **macOS (Homebrew):** `brew install pango`
- **Windows:** follow the [WeasyPrint install guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)

### 5b. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Set the Django environment variables before running the project.
The `.env.example` file lists every variable the project reads. Django does
not load `.env` files automatically, so export the values in your shell:

```bash
export DJANGO_SECRET_KEY="your-secure-secret-key"
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
```

Generate a secure secret key using:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7. Apply Migrations

```bash
python3 manage.py migrate
```

### 8. Create a Superuser

```bash
python3 manage.py createsuperuser
```

### 9. Run the Development Server

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

The test suite currently contains **111 tests**.

Check Django configuration:

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
- Login-required access to protected views
- Portfolio ownership validation
- Connection and endorsement authorization checks
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

This project is developed for educational and portfolio purposes.