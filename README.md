# Delivery Tracker
## _With a PYNQ-Z2 board and a webcam, check out what's going on in front of your home or when your packages are delivered._

The Delivery Tracker Team has developed an application that notifies when a user's packages are delivered and monitors their door for different activities with a web camera. The application leverages the OpenCV Machine Learning and Facial recognition libraries, a webcam, a PYNQ-Z2 FPGA development board, and the Django web framework. Facial and body detection can detect activities, detect when a person drops off a package at the front door, and take a snapshot. The application supports a backend database that stores events and pictures and allows users to view and manage them.

## Features

- Monitors a user’s home exterior for activity with a web camera and produces facial recognition analyses of events with OpenCV libraries.
- Hosted locally with a backend database that stores events & photos.
- Supports user registration and authentication for a user with their email and device #ID.
- Protected routes allow the user to securely view or delete their events and photos.
- Provides an informative user guide to set up their PYNQ-Z2 board and webcam.
- User-friendly interface to look through events and photos, and supports functionality to filter events by date.
- Allows the user to update their information, device #ID, and password.
- Sends notifications of events to the user through their email address.
- Produces a live feed of notifications to alert the user of new events on the web interface.

## Tech

Delivery Tracker uses a number of open source projects to work properly:

- [Python]
- [Django]
- [PostgreSQL]
- [django-tables2]
- [django-crispy-forms]
- [django-notifications]
- [Bootstrap]
- [Tailwind CSS]
- [Alpine.js]
- [JavaScript]
- [PYNQ-Z2]
- [Jupyter Notebooks]
- [OpenCV]

## Installation

Delivery Tracker requires [Django](https://www.djangoproject.com/download/) v4.1.2, [PostSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) v14.6,  [PYNQ-Z2](http://www.pynq.io/board.html) v3.0.1, and a [Logitech C270](https://www.logitech.com/en-us/products/webcams/c270-hd-webcam.960-000694.html) webcam to run.

Setting up the database.

```sh
cd C:\Program Files\PostgreSQL\14\bin
psql -U postgres -W
postgres=# CREATE USER yourname;
postgres=# create database deliverytracker;
```

Django Project Setup.
Cloning the repo and creating the virtual environment.
```sh
git clone https://github.com/waringk/DeliveryTracker.git
cd DeliveryTracker
py -m venv .
./scripts/activate.ps1
pip install -r requirements.txt
cd apps
```

Creating the environment variables.
```sh
cd .\apps\config
```
Create a file named ".env" in the config folder.
```
.
└── deliverytracker/
    ├── .git
    ├── .idea
    └── apps/
        ├── __pycache__
        └── config/             Add your .env file here
            └── .env
```
Open the .env file and set the environment variables.
```code
SECRET_KEY=[Your Django Key]
DATABASE_NAME=deliverytracker
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
EMAIL_PASSWORD=[Your email password]
```

Run migrations.
```sh
cd apps
python manage.py makemigrations
python manage.py migrate
```

## Running the server
Run the application locally.
```sh
cd apps
python manage.py runserver 0.0.0.0:8000
```

## Setting up and running the PYNQ-Z2 processes.
View the support page of the Delivery Tracker when the server is running.

   [Python]: <https://www.python.org/>
   [Django]: <https://www.djangoproject.com/>
   [PostgreSQL]: <https://www.postgresql.org/>
   [django-tables2]: <https://github.com/jieter/django-tables2>
   [django-crispy-forms]: <https://github.com/django-crispy-forms/django-crispy-forms>
   [django-notifications]: <https://github.com/django-notifications/django-notifications>
   [Bootstrap]: <https://getbootstrap.com/>
   [Tailwind CSS]: <https://tailwindcss.com/>
   [Alpine.js]: <https://alpinejs.dev/>
   [JavaScript]: <https://www.javascript.com/>
   [PYNQ-Z2]: <http://www.pynq.io/>
   [Jupyter Notebooks]: <https://jupyter.org/>
   [OpenCV]: <https://opencv.org/>
