## Book Store Website && Mobile App

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Run](#run)

## General info
- This project let's admin or staff users add Products, Categories, Authors, Publisher, Shipping Fees and more
- It allows users to order some items and add them in the shopping cart and only we ask them to login on checkout
- Once the user submit an order he recieve and E-mail that has the order info
- Once the order status changes from 'Waiting' to 'On Delivery' the customer recieves an SMS
- Custom Admin statistics page that has everything he might need along with visitors tracking

## Technologies
Project is created with:
* Django
* Django Rest Framework
	
## Run
To run this project locally, run this command

```
$ pip install -r requirements.txt
$ python manage.py makemigrations --settings=bookstore.settings.local
$ python manage.py migrate --settings=bookstore.settings.local
$ python manage.py runserver --settings=bookstore.settings.local
```
