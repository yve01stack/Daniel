import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
   # Database initialization
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = True
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE=False
    JWT_ACCESS_CSRF_COOKIE_NAME = 'csrf_access_token'
    JWT_REFRESH_CSRF_COOKIE_NAME = 'csrf_refresh_token'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    ACCOUNT = {
        'Gabon': {'account_number': '15195965232', 
            'account_name': 'Daniel Burgest',
            'account_email': 'mesachats.chine@gmail.com',
            "coordinates": {
                "longitude": 9.4418849,
                "latitude": 0.4086518,
            },
        }
    }
    
    SERVER_URL = 'http://localhost:5000/'
    FRONTEND_URL = 'http://localhost:5173/user/profile'

    #Sending email via api and RAPIDAPI
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')   
    REPLY_TO_EMAIL = os.environ.get('REPLY_TO_EMAIL')   
    SENDER_NAME = "Mes Achat en Chine" 
    SEND_VIA_API = False
    
    ALIEXPRESS_URL = os.environ.get('ALIEXPRESS_URL')
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
    FIREBASE_MAILER_URL = os.environ.get('FIREBASE_MAILER_URL')
  
    # flask mail sender
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    HANDLER_EMAILS = ['programm01dev@gmail.com', 'mesachats.chine@gmail.com']

  