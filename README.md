# Bus Reservation System

A modern, robust, and premium Bus Reservation System built with **Django** and **MySQL**. This project features a comprehensive role-based access control system for Administrators, Staff members, and Customers.

## 🚀 Features

### 👤 User Roles
- **Administrator:** Full control over buses, routes, user management, and staff assignments.
- **Staff:** Specialized dashboard to manage trip schedules, seat availability, and passenger lists.
- **Customer:** Clean interface to search for buses, book seats, manage profiles, and view booking history.

### 🛠️ Key Functionalities
- **Dynamic Search:** Find buses based on source, destination, and date.
- **Secure Booking:** Real-time seat allocation and booking management.
- **Role-Based Portals:** Custom dashboards for each user type.
- **Modern UI:** Responsive design with a focus on user experience (inspired by premium platforms like redBus).
- **Environment Security:** Sensitive credentials managed via `.env` for production readiness.

## 💻 Tech Stack
- **Backend:** Python / Django
- **Database:** MySQL
- **Frontend:** HTML5, CSS3 (Vanilla CSS), JavaScript
- **Security:** python-dotenv for environment variable management

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL Server

### 1. Clone the repository
```bash
git clone https://github.com/miyat0/bus_reservation_project.git
cd bus_reservation_project
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your database credentials:
```env
DB_NAME=bus_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ for a seamless travel experience.*
