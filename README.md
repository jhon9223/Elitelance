Elitelance 🚀
Elitelance is a full-featured freelancing marketplace web application built with Django. It connects clients and freelancers, allowing job posting, bidding, profile management, and AI-assisted content generation.

🔹 Features

User authentication with role-based access (Client, Freelancer, Manager)
Client dashboard for posting and managing jobs
Freelancer dashboard for browsing jobs and submitting proposals
Public profile system for freelancers
AI-powered job description and proposal generation
Notification system
Profile management with image upload


🔹 Tech Stack

Backend: Django, Django REST Framework
Frontend: HTML, CSS, JavaScript
Database: SQLite
Deployment: PythonAnywhere
AI Integration: Hugging Face API


🔹 Project Structure
elitelance/
│
├── accounts/
├── jobs/
├── dashboard/
├── core/
├── api/
├── templates/
├── static/
├── uploads/
├── manage.py


🔹 Installation (Local Setup)

Clone the repository:

git clone https://github.com/jhon9223/Elitelance.git
cd Elitelance


Create virtual environment:

python -m venv env
env\Scripts\activate   (Windows)


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Run server:

python manage.py runserver


🔹 Environment Variables
Add your Hugging Face API token in settings.py:
HUGGINGFACE_API_TOKEN = "your_token_here"


🔹 Demo Accounts
You can use the following accounts to test different roles:

Freelancer

Username: ebin
Password: blackandwhite123

Client

Username: nextgen_softwares
Password: blackandwhite123

Manager

Username: _liam
Password: blackandwhite123

Admin

Username: johnn
Password: john123


🔹 Key Functionalities

Role-based redirection after login
Profile completeness tracking
Image upload and media handling
AI content generation for:

Job descriptions
Freelancer proposals




🔹 Deployment
The project is deployed on PythonAnywhere.
Steps:

Upload project or clone from GitHub
Install requirements
Run migrations
Configure static and media files
Add API token
Reload web app


🔹 Future Improvements

Payment integration
Chat system between client and freelancer
Advanced AI suggestions
Email notifications


🔹 Author
John Nj
GitHub: https://github.com/jhon9223
LinkedIn: https://www.linkedin.com/in/dev-johnnj
project live/deployment link: https://john2293.pythonanywhere.com/
