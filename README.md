# Vendor Management System

## Table of Contents
 
- [Description](#description)
- [Setup](#setup)
- [Run](#run)
- [Test](#test)
- [API Documentation](#api-documentation)
- [Contact](#contact)
 

## Description  

The Vendor Management System is built using Django REST Framework and Celery, offering robust features for email notifications and task scheduling. This system manages vendor profiles, tracks purchase orders, and calculates key performance metrics such as on-time delivery rate, quality ratings, response time, and fulfillment rate.  

Key functionalities include:  
- **Real-time Notifications:** Sends email notifications to vendors when new purchase orders are issued.  
- **Deadline Reminders:** Notifies vendors about pending deliveries as deadlines approach.  

### Technology Stack:  
- **Authentication:** JWT (JSON Web Token)  
- **Database:** PostgreSQL  
- **Task Queue:** Celery for scheduling and executing background tasks efficiently.  




## Setup
To use Vendor Management System use below repo
 
```
git clone https://github.com/TejaVenkatBalla/vms.git
cd vms

```

It is recommended to ceate virtual environments while installing Python applications

For Windows,

* Create virtual environent using `python -m venv "path"`
* Activate virtual envrionment using `venv\Scripts\activate.bat`

For Linux, 
* Create virtual environment using `virtualenv venv`
* Activate using source `venv/bin/activate` ( `source venv/bin/activate` )

Install the dependency libraries for Vendor Management System using
`pip install -r requirements.txt`

## Run
After performing any changes in model, use `python manage.py makemigrations`

To reflect changes in database, use `python manage.py migrate`

To create user, use `python3 manage.py createsuperuser`

To run server
```
python manage.py runserver
```

## Test
To execute test scripts, use `python3 manage.py test`

## API Documentation
Link to the [Postman Collection](https://github.com/TejaVenkatBalla/vms/blob/main/vms.postman_collection.json)

### User Signup/Signin Endpoints

#### User Registration

- **Method:** POST  
- **URL:** `http://127.0.0.1:8000/api/register/`  
- **Request Body:** JSON containing `username`, `password`, and `email`:  
    ```json
    {
        "username": "tb",
        "password": "rander",
        "email": "tb@gmail.com"
    }
    ```  
- **Response:** On successful registration, returns a confirmation message along with `refresh` and `access` tokens:  
    ```json
    {
        "message": "User Successfully Registered",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDM1MjUwOSwiaWF0IjoxNzM0MjY2MTA5LCJqdGkiOiJlOTU1NGVlYTE5YmI0MGY4OTdhMDAwZTE0MTljYjM4NiIsInVzZXJfaWQiOjN9.GBv6_bdGbyYL1VEHSCMMnIio9U8a-k9-SebXOIkugCQ",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MjY2NDA5LCJpYXQiOjE3MzQyNjYxMDksImp0aSI6ImIzYWU5MmIyMjBlNDRmNDQ5ZWIzOWJkZjUwZWM3YjNiIiwidXNlcl9pZCI6M30.vfAxmYGZSPKbD9WRA4xOXl7vMxaRH-CLcchk7CFTago"
    }
    ```  

#### User Login

- **Method:** POST  
- **URL:** `http://127.0.0.1:8000/api/login/`  
- **Request Body:** JSON containing `username` and `password`:  
    ```json
    {
        "username": "tballa",
        "password": "admin"
    }
    ```  
- **Response:** On successful authentication, returns `refresh` and `access` tokens:  
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDM1MTk3MCwiaWF0IjoxNzM0MjY1NTcwLCJqdGkiOiJjYmJkOGVjY2ExZDE0NTAzYTk0MDdiODU2MDQ4Yzc0NyIsInVzZXJfaWQiOjF9.Qfx-f-tI_tf_SZYBB_qOCpTjfC2PJlu7-PGc4TVHaGU",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MjY1ODcwLCJpYXQiOjE3MzQyNjU1NzAsImp0aSI6IjA1MWJhMTc5MDg0MjRkODM5NmJiZDJmNWFhZTFhMDI5IiwidXNlcl9pZCI6MX0.R_N3vzBwGkwU3NJhF52lLe_k7BwOQLalGo0y_7ojDKI"
    }
    ```

### Vendor Profile Management Endpoints
- **List all vendors:** GET `/api/vendors/`
- **Retrieve a specific vendor's details:** GET `/api/vendors/{vendor_id}/`
- **Create a new vendor:** POST `/api/vendors/`
- **Update a vendor's details:** PUT `/api/vendors/{vendor_id}/`
- **Delete a vendor:** DELETE `/api/vendors/{vendor_id}/`
- **Vendor Performance:** GET `/api/vendors/{vendor_id}/performance/`

### Purchase Order Tracking Endpoints
- **List all purchase orders:** GET `/api/purchase_orders/`
- **Retrieve details of a specific purchase order:** GET `/api/purchase_orders/{po_id}/`
- **Create a purchase order:** POST `/api/purchase_orders/`
- **Update a purchase order:** PUT `/api/purchase_orders/{po_id}/`
- **Delete a purchase order:** DELETE `/api/purchase_orders/{po_id}/`
- **Update Acknowledgment:** POST `/api/purchase_orders/{po_id}/acknowledge/`

### Endpoint to Schedule a Task (Vendor Deadline Reminder)
 
- **URL:** GET `/api/scheduler/`  
- **Purpose:** Schedule a reminder for a vendor about the delivery deadlines.  


For all endpoints, you need to include the obtained access token in the `Authorization` header with the prefix "Bearer".

For example:
```
Authorization: Bearer <access token>
```
Make sure to replace `{vendor_id}` and `{po_id}` with the actual IDs of vendors and purchase orders respectively.

## Contact
Email: tejavenkatballa@gmail.com
contact: +91 9539530165 
