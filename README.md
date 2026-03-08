# SmartPrint Management API

A production-ready **Printshop Workflow Management System** built with **Django REST Framework (DRF)**.  
SmartPrint enables printshops to manage customers, orders, and production workflows with role-based access and activity logging.

---

## Features
- **Authentication & Authorization**
  - JWT-based authentication (`djangorestframework-simplejwt`)
  - Role-based access control (Admin, Designer, Editor, Printer, Finisher, Delivery Staff)
- **Customer & Order Management**
  - Manage customer profiles and contact details
  - Orders with multiple print jobs
  - Track order status (`pending`, `in_production`, `completed`, `delivered`)
- **Production Workflow**
  - Specialized roles for staff:
    - Designer → Upload and finalize artwork
    - Editor → Review and approve designs
    - Printer → Handle printing tasks
    - Finisher → Post-print processing (cutting, binding, laminating)
    - Delivery Staff → Package and deliver orders
- **Activity Logging**
  - Tracks all actions (create/update/delete) for accountability
- **Production-Ready Enhancements**
  - Pagination, filtering, and search
  - Dockerized deployment
  - Redis caching
  - CI/CD pipeline ready
  - Error monitoring with Sentry

---

## Tech Stack
- **Backend**: Django, Django REST Framework  
- **Auth**: JWT (SimpleJWT)  
- **Database**: PostgreSQL   
- **Caching**: Redis  
- **Deployment**: Docker, Gunicorn, Nginx  
- **Testing**: Pytest, DRF test client  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Kwanusu/smart_print_shop.git
cd smartprint-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

---

## Authentication
- Obtain JWT token:
  ```
  POST /api/token/
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- Refresh token:
  ```
  POST /api/token/refresh/
  ```

Use the token in headers:
```
Authorization: Bearer <your_token>
```

---

## API Endpoints

| Endpoint                  | Method | Description                          | Role Required |
|---------------------------|--------|--------------------------------------|---------------|
| `/api/token/`             | POST   | Obtain JWT token                     | Any user      |
| `/customers/`             | GET    | List customers                       | Admin         |
| `/orders/`                | POST   | Create new order                     | Admin         |
| `/orders/{id}/jobs/`      | GET    | List jobs in an order                | Authenticated |
| `/jobs/{id}/design/`      | PATCH  | Mark job as design complete          | Designer      |
| `/jobs/{id}/approve/`     | PATCH  | Approve job for printing             | Editor        |
| `/jobs/{id}/print/`       | PATCH  | Mark job as printed                  | Printer       |
| `/jobs/{id}/finish/`      | PATCH  | Mark job as finished                 | Finisher      |
| `/orders/{id}/deliver/`   | PATCH  | Mark order as delivered              | Delivery Staff |
| `/activity/`              | GET    | View activity logs                   | Admin/Manager |

---

## Testing
Run tests with:
```bash
pytest
```

---

## Docker Setup
Build and run with Docker:
```bash
docker-compose up --build
```

---

## Deployment
- Use **Gunicorn** + **Nginx** for production  
- Configure **PostgreSQL** for database  
- Add **Redis** for caching  
- Integrate **Sentry** for error monitoring  
- Set up **CI/CD** with GitHub Actions or GitLab CI  

---

## Contributing
1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Add feature"`)  
4. Push to branch (`git push origin feature-name`)  
5. Open a Pull Request  

---

## Contact
For inquiries, support, or collaboration:  
- **Email**: kwanusujoseph@gmail.com  
- **Phone**: +254-725-439-354  
- **Website**: [www.smartprint.com](http://www.smartprint.com)  
- **Address**: SmartPrint HQ, Nairobi, Kenya  

---

##  License
This project is licensed under the MIT License.
