# Socialfly Instagram Clone
Socialfly is a Instagram Clone made by Django Web Framework and channel

LINK : https://techkynewz.com
 ***
## Features 
 - Most of all instagram features are their
 - You can **create** post **delete** and report or **like** comment on the post
 - Every action you make is tracked and send **notification** instantly that makes it **realtime** also configured for **PWA**
 -  A  **private Dms** are also included so that you can chat with your friends **privately**
- **User recommendation system** is also included  
 - Authentication is include with email verification for you account with **django allauth** 
  - Hosted on **AWS** with **s3 Bucket** for storage on **ngnix server**  
 

***
## What Technology Used

### FrontEnd
 - HTML5
 - CSS
 - JavaScript
 - Bootstrap  snippets
 - Jquery 

###  Backend

 - Django Python Web Framework
 - PostgreSQL for Database
 - Redis server(For Messaging)
 - Django Channels (WebSocket)
 - Sendgrid Email API for sending Emails
 - Google,GitHub,Discord for Oauth  
***

## Getting started
###   Requirements
 - Python 3.6+
 - pip
 - virtualenv 
 - Redis server(For Messaging)
 - Django Channels (WebSocket)

###  Installation
```bash
# Clone the repository
git clone https://github.com/Abhishek-Gawade-programmer/socialfly-instagram-clone

# Enter into the directory
cd socialfly-instagram-clone/

# Create virtual environment 
virtualenv env

# Activate virtual environment 
source env/bin/activate

# Install the dependencies
pip install -r requirements.txt


# Check migrations.
python manage.py makemigrations

# Apply migrations.
python manage.py migrate

#Load Test Data
python manage.py loaddata fixture.json 
 #admindjango dfgdfg@#4rjsnv(superuser)
 #tempuser dfgdfg@#4rjsnv 

#Starting the application
python manage.py runserver

```
###  Configuration
Create `.env` file in cwd and add the following
```conf
#WEB PUSH NOTIFIACTION FROM BROWSER(optional)
SECRET_KEY=""
VAPID_PUBLIC_KEY=""
VAPID_PRIVATE_KEY=""
VAPID_ADMIN_EMAIL=""

#AWS s3 bucket secrets(optional)
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_STORAGE_BUCKET_NAME=""

#Email Settings
EMAIL_BACKEND=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''

```
###  Start redis Broker 
``` bash
cd redis
src/redis-server
#redis server will start at localhost:6863
```









