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

## Contact
Email: tejavenkatballa@gmail.com
contact: +91 9539530165 
