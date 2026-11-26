# Online Quiz Platform

Beginner-friendly quiz application using Django, HTML, CSS, JavaScript and SQLite.

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for initial package installation and Google Fonts

## Setup (Windows)
1. Extract the ZIP file.
2. Open the `OnlineQuizPlatform` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   `py -m venv venv`
5. Activate it:
   PowerShell: `venv\Scripts\Activate.ps1`
   Command Prompt: `venv\Scripts\activate.bat`
6. Install Django:
   `py -m pip install -r requirements.txt`
7. Create database tables:
   `py manage.py makemigrations quiz`
   `py manage.py migrate`
8. Create administrator:
   `py manage.py createsuperuser`
9. Start the server:
   `py manage.py runserver`
10. Open http://127.0.0.1:8000/ in your browser.
11. Open http://127.0.0.1:8000/admin/ and log in with your superuser.
12. Add a Quiz and add its Questions using the inline question form. Set `is active` to enabled.
13. Register a student account on the main website and take the quiz.

## Notes
- The quiz uses four options (A-D) and one correct option per question.
- The timer is checked in the browser and the server checks the stored attempt start time when the quiz page is loaded. For a production examination system, strengthen server-side timeout enforcement and add robust answer storage, audit logs, and deployment security.
- This starter project allows students to take the same quiz more than once.
- Before deployment, set a secure SECRET_KEY, DEBUG=False, configure ALLOWED_HOSTS, HTTPS, static files, and production database settings.
