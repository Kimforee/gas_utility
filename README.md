# Gas Utility Service Management System

## Overview
This Django application addresses the challenges faced by a gas utility company in managing high volumes of customer service requests. The application allows:

- **Customers** to submit service requests, track their status, and view account information.
- **Customer support representatives** to manage requests and provide efficient support.

Key technologies used include:
- **Django** for backend development.
- **PostgreSQL** for database management.
- **Redis** for asynchronous task queuing.
- **Celery** for handling background jobs.
- **WSL** for running Celery and Redis on Windows.

The system effectively manages high customer volumes using asynchronous processing, ensuring reduced wait times and improved service quality.
following is the adminstration ss for customer management
![image](https://github.com/user-attachments/assets/1b91dc6a-2974-4d77-9678-63a62532cf46)

---

## Features
1. **Service Request Submission**: Customers can submit detailed service requests with file attachments.
2. **Request Tracking**: Customers can monitor the status of their requests in real time.
3. **Support Management Tool**: Customer support representatives can view and update service requests(using django builtin tool called django-administration).
4. **Asynchronous Processing**: High-volume updates are handled efficiently using Celery and Redis.

---

## How the High Volume Issue is Solved
To handle a high number of customer requests:
- **Asynchronous Processing**: Celery offloads heavy tasks like notifications and updates to a background queue managed by Redis.
- **Efficient Database Design**: PostgreSQL ensures quick and reliable data storage and retrieval.

---

## Installation
### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis (for Celery)
- WSL (for running Celery and Redis on Windows)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Kimforee/gas_utility
   cd gas_utility
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate   # On Windows
   ```

3. Install dependencies:
   - For Windows:
     ```bash
     pip install -r requirements.txt
     ```
   - For Linux/WSL:
     ```bash
     pip install -r linux_requirements.txt
     ```

4. Configure the `.env` file with your database and Redis credentials ( please find the .env template for the setup ):
   ```env
   SECRET_KEY=your-secret-key (to be found inside the django application)
   DEBUG=True
   DATABASE_URL=postgres://username:password@hostname:port/database
   CELERY_BROKER_URL=redis://hostname:port/0
   ```

5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run Redis on WSL after installation:
   ```bash
   sudo service redis-server start
   ```

8. Start Celery workers:
   ```bash
   celery -A gas_utility worker --loglevel=info
   ```

9. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

---

## Usage
### Submitting a Service Request
Endpoint: `POST api/service_requests/submit/`

Payload example:
![image](https://github.com/user-attachments/assets/1f47fe8e-00fa-493a-9bec-2599a177357b)

### Tracking a Service Request
Endpoint: `GET api/service_requests/manage/5/`

response:
![image](https://github.com/user-attachments/assets/3a97aadb-9849-4973-908c-3dea72f5e6c2)

### Support Representative Actions
- **View Requests**: `GET /support/requests/`
- **Update Request**: `PATCH api/service_requests/manage/1/`

View :
![image](https://github.com/user-attachments/assets/89784671-858c-4663-8253-db5382587ce8)

Update :
![image](https://github.com/user-attachments/assets/513bb88c-692d-4633-aeac-b32cb2295332)

---

## Screenshots
### 1. Submitting a Service Request
![image](https://github.com/user-attachments/assets/db5c8bce-46bb-430b-af5b-5687018db987)

### 2. Tracking a Request
![image](https://github.com/user-attachments/assets/f445eaa2-1b54-4d06-8c70-ff6f4578fc1d)

### 3. Managing Requests as Support Representative
![image](https://github.com/user-attachments/assets/ccf68519-b891-4944-8b77-2fc96a43ea8f)

---

---
## Future Enhancements
- Add email/SMS notifications for request updates.
- Implement role-based access control for enhanced security.
- Develop a user-friendly frontend interface.

---

## Conclusion
This application solves the problem of high customer volumes and long wait times by leveraging Django’s robust framework and integrating asynchronous processing with Celery and Redis.

