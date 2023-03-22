# hypnobot


* This is a Django web application that allows users to intract with rest endpoints.

* Installation

* Before you can use the application, you need to install Django and all its dependencies. You can do this by running the following command:

-> pip install -r requirements.txt

* This will install all the required packages listed in the requirements.txt file.

* Configuration

* The application uses a PSQL database. If you want to use a different database, you can change the database settings in the settings.py file.

* To configure other settings for the application, you can create a .env file in the root directory of the application and set any environment variables you need. An example .env file might look like this:

SALT=xxxxxxx
SECRET_KEY=xxxxx
CONFIG=development
DB_NAME=xxxxxxx
DB_USER=xxxxxx
DB_PASSWORD=xxxxxx
DB_HOST=xxxxxx
DB_PORT=xxxxxx
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = xxxxxxx
EMAIL_HOST_PASSWORD = xxxxx
IP = xxxxxxx


* Usage
To start the application, run the following command:


-> python manage.py runserver

* This will start the development server, which you can access by opening a web browser and navigating to http://localhost:8000/.

