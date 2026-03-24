🚀 EliteLance – Freelancing Marketplace
EliteLance is a modern freelancing platform where clients can post jobs and freelancers can apply, collaborate, and complete projects efficiently.
Built with Django, this project demonstrates a full-stack web application with role-based access, dashboards, notifications, and REST APIs.

🌐 Live Demo


📸 Preview


🚀 Features
🔐 Authentication & Roles

User registration & login system
Role-based access:

👤 Client
🧑‍💻 Freelancer
🧑‍💼 Manager




💼 Job Management
Clients can:

Post jobs
View proposals
Manage job listings

Freelancers can:

Browse jobs
Apply with proposals


📊 Dashboards
👤 Client Dashboard

Total jobs overview
Proposal tracking
Recent job activity

🧑‍💻 Freelancer Dashboard

Total proposals
Accepted proposals
Active contracts
Completed work

🧑‍💼 Manager Dashboard

Platform analytics
User, job, and contract insights


🔔 Notification System

Real-time styled UI notifications
Notification bell icon
Dynamic updates
Clean toast alerts


🎨 UI/UX

Modern glassmorphism design
Aurora gradient background
Smooth animations & transitions
Fully responsive layout


⚙️ Admin Panel

Custom user model with roles
Client & Freelancer profile management
Profile image preview in admin


🔌 API (Django REST Framework)

Job listing API
Token-based authentication
Serializer-based architecture


🛠️ Tech Stack

Backend: Django, Django REST Framework
Frontend: HTML, Tailwind CSS
Database: SQLite (development)
Version Control: Git & GitHub


📁 Project Structure
elitelance/
│
├── accounts/        # User & profile management
├── jobs/            # Job & proposal logic
├── dashboard/       # Role-based dashboards
├── api/             # REST APIs
├── templates/       # HTML templates
├── static/          # Static files
├── manage.py
└── requirements.txt


⚙️ Setup Instructions
# Clone repository
git clone https://github.com/jhon9223/Elitelance
cd Elitelance

# Create virtual environment
python -m venv env

# Activate environment (Windows)
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver


🚀 Future Improvements

Payment integration (Stripe/Razorpay)
Real-time chat system
Email notifications
Job recommendations
Advanced analytics dashboard


🤝 Contributing
Feel free to fork this repository and contribute!

📧 Contact

GitHub: https://github.com/jhon9223
LinkedIn: https://www.linkedin.com/in/dev-johnnj


⭐ Show your support
If you like this project, give it a ⭐ on GitHub!
