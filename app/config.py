import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:PENGchuan824@localhost/todo_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
