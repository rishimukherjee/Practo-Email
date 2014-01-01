# Practo Email

Easily send emails to your patients.

## Usage

This application was created and tested in Django 1.5 with MySql.

## Setup

Create a database named `mailmaster` in MySQL.

Configure according to this link if you want to use some other database engine:
[django docs](https://docs.djangoproject.com/en/dev/intro/tutorial01/#database-setup)

Open the settings.py in the application and edit the following fields.
    
  * `EMAIL_HOST` Email server address. smtp.gmail.com for gmail.
  * `EMAIL_HOST_USER` You email id.
  * `EMAIL_HOST_PASSWORD` You email password.
  * `EMAIL_PORT` 587 for gmail.
  * `EMAIL_USE_TLS` True for making it secure else False.

In the `DATABASE` section of the settings.py,

  * `USER` Your mysql username.
  * `PASSWORD` Your mysql password.
  
Type the following commands:

    python manage.py syncdb
    python manage.py runserver
    
Visit
[localhost](http://127.0.0.1:8000/)
