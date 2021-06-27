# PetStore
## Overview
RESTful web app for pet store. It is built using Django framework to manage server functionality. Django REST framework library to manage API endpoints. SQLite to manage database engine.
## Refrances 
- Python Style Guide. [here](https://www.python.org/dev/peps/pep-0008/#introduction)
- Django official documentation.[here](https://docs.djangoproject.com/en/3.2/contents/)
- Django REST framework documentation. [here](https://www.django-rest-framework.org/tutorial/quickstart/)
## Install project
### Install libraries 
     pip install -r requirements.txt
### Database midrations 
     python manage.py migrate
### Run web server 
     python manage.py runserver
### Run tests 
     python manage.py test
### Create covarage report 
     python -m coverage run --source='.' manage.py test
### View covarage report 
     python -m coverage repor
## API Endpoints
### Pets
* GET: **/store/pets/?breed=** (List all pets with option of breed filtering)
* POST: **/store/pets/** (Create new pet)
* GET/PUT/DELETE: **/store/pets/{pet-id}/** (Pet retrieve, update and destroy endpoint)

### Order
* POST: **/store/orders/** (Create new order)
* GET: **/store/orders=** (List all orders)
