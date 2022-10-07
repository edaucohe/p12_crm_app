# Project 12 - CRM app

## Contents
- [Keywords](#keywords)
- [Description](#description)
- [Installation](#installation)
- [Use](#use)
- [Helpful links](#links)

## Keywords <a class="anchor" id="keywords"></a>
- Customer Relationship Management (CRM)
- User, customer, contract, event
- Application Programming Interface (API)
- Django Rest Framework (DRF)

## Description <a class="anchor" id="description"></a>

"Project 12 - CRM app" is a project of OpenClassrooms "Python Application Developer" 
course leading to a qualification.

This project aims to implement a CRM based on an API using DRF.

The app allows three kind of users: 
- Management user.
- Sales user.
- Support user.

Every user has different permissions concerning customers, contracts and events information:
- **Management user** has all permissions to read, create, update and delete other users, 
and customers, contracts and events information too. 
- **Sales user** has all permissions to read, create, update and delete contracts and events of a customer assigned.
- **Support user** has all permissions to read, create, update and delete events of a customer assigned.
- **All users** can see a list of all customers.

The main technical requirements are:
- Create an API REST with Django Rest Framework (DRF).
- Implement authorization according to role of user (Management/Sales/Support).
- Implement logging feature.
- Implement filter feature.

You can also see technical documentation (French version) in 
`../p12_crm_app/documentation/`.

## Installation <a class="anchor" id="installation"></a>

Python version : 3.9.4

To get project, launch :
```
git clone https://github.com/edaucohe/p12_crm_app.git
```

To create virtual environment, go into the folder `../p12_crm_app/` and launch :
```
python -m venv env  
```

To activate virtual environment, launch :

- In windows `source env/Scripts/activate`
- In Linux `source env/bin/activate`

To install dependencies file `requirements.txt`, launch :
```
pip install -r requirements.txt
```

## Use <a class="anchor" id="use"></a>

### Launch and stop local server

To start API, go into the folder `../p12_crm_app/crm/` and launch:
```
python manage.py runserver  
```

If you want to stop local server, type *ctrl + c* in terminal.

### Endpoints

Concerning endpoints, they are formed by the root `http://127.0.0.1:8000/` followed by an URI. 
You can find here below the main URI list:

| #   |    Functionality     | HTTP Request |                    URI                    |
|-----|:--------------------:|:------------:|:-----------------------------------------:|
| 1   |     User sign up     |     POST     |                 /signup/                  |
| 2   |      User login      |     POST     |                  /login/                  |
| 3   |      User list       |     GET      |                  /users/                  |
| 4   |    Create an user    |     POST     |                  /users/                  |
| 5   |    Customer list     |     GET      |                /customers/                |
| 6   |   Create customer    |     POST     |                /customers/                |
| 7   | Update customer info |     PUT      |             /customers/{id}/              |
| 8   |   Delete customer    |    DELETE    |             /customers/{id}/              |
| 9   |    Contract list     |     GET      |        /customers/{id}/contracts/         |
| 10  |   Create contract    |     POST     |        /customers/{id}/contracts/         |
| 11  |   Update contract    |     PUT      |      /customers/{id}/contracts/{id}       |
| 12  |   Delete contract    |    DELETE    |      /customers/{id}/contracts/{id}       |
| 13  |      Event list      |     GET      |          /customers/{id}/events/          |
| 14  |     Create event     |     POST     |          /customers/{id}/events/          |
| 15  |     Update event     |     PUT      |        /customers/{id}/events/{id}        |
| 16  |     Delete event     |    DELETE    |        /customers/{id}/events/{id}        |

Also, you can find here below exemples of URI concerning filters. 

**Customer filters:**

| #   |    Functionality    | HTTP Request |                   URI                    |
|-----|:-------------------:|:------------:|:----------------------------------------:|
| 17  | Company name filter |     GET      | /customers/?company_name=johnny+company  |
| 18  |    Email filter     |     GET      |          /customers/?email=tony          |

**Contract filters:**

| #   |     Functionality     | HTTP Request |                        URI                        |
|-----|:---------------------:|:------------:|:-------------------------------------------------:|
| 19  |  Company name filter  |     GET      | /customers/2/contracts/?company_name=tony+company |
| 20  | Customer email filter |     GET      |   /customers/2/contracts/?email=tony%40tony.com   |
| 21  |   Min amount filter   |     GET      |      /customers/2/contracts/?min_amount=100       |
| 22  |  Payment due filter   |     GET      |  /customers/2/contracts/?payment_due=2022-10-30   |

**Contract filters:**

| #   |     Functionality     | HTTP Request |                      URI                       |
|-----|:---------------------:|:------------:|:----------------------------------------------:|
| 23  |  Company name filter  |     GET      | /customers/2/events/?company_name=tony+company |
| 24  | Customer email filter |     GET      |   /customers/2/events/?email=tony%40tony.com   |
| 25  |   Event date filter   |     GET      |   /customers/2/events/?event_date=2023-01-30   |

When local server is launched, you can go to your Postman account and test endpoints 
according to **API documentation** (See [Helpful links](#links)).

### User access

Concerning management users already registered in DB, you can find here below their contact details 
in order to access to **Admin page** (See [Helpful links](#links)):

| Username |  Password   | User role  |
|:--------:|:-----------:|:----------:|
|  admin   |   hiadmin   | Management |
|   anne   | SECRETanne. | Management |

Concerning sales and support users already registered in DB, you can find here below their contact details 
in order to access thanks to Postman:

| Username |   Password   | User role |
|:--------:|:------------:|:---------:|
|   mari   | SECRETmari.  |   Sales   |
|  manon   | SECRETmanon. |   Sales   |
|   john   | SECRETjohn.  |  Support  |

## Helpful links <a class="anchor" id="links"></a>

DRF installation and settings:
https://www.django-rest-framework.org/

JWT installation and settings:
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html

ViewSet methods exemples:
https://ilovedjango.com/django/rest-api-framework/views/viewset/

DRF Nested routers installation, explanation and exemples: 
https://github.com/alanjds/drf-nested-routers

Python logging documentation:
https://docs.python.org/3/library/logging.html

Django filter documentation:
https://django-filter.readthedocs.io/en/stable/index.html

API documentation:
https://documenter.getpostman.com/view/22241212/2s83zfR64P

Admin page:
http://127.0.0.1:8000/admin/login/?next=/admin/
