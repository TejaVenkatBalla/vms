# Vendor Management System

## Table of Contents
 
- [Description](#description)
- [Setup](#setup)
- [Run](#run)
- [Test](#test)
- [API Documentation](#api-documentation)
- [Contact](#contact)
 
## Description
Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles,
track purchase orders, and calculate vendor performance metrics.

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

### Auth_token Endpoint
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api-token-auth/`
- **Body:** JSON with username and password
    ```json
    {
        "username": "tballa",
        "password": "admin"
    }
    ```
- **Response:** 
    ```json
    {
        "token": "b0d1cd2de6ae71ea0573ae83861d3a35bea75a09"
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

For all endpoints, you need to include the obtained token in the `Authorization` header with the prefix "token".

For example:
```
Authorization: token b0d1cd2de6ae71ea0573ae83861d3a35bea75a09
```
Make sure to replace `{vendor_id}` and `{po_id}` with the actual IDs of vendors and purchase orders respectively.

## Contact
Email: tejavenkatballa@gmail.com
contact: +91 9539530165 
