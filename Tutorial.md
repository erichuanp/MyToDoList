# MyToDoList App Development Tutorial
This is a tutorial for my full stack project MyToDoList. 
## Understand the structure and steps

```
[User] <---> [Vue.js Frontend] <---> [Flask Backend API] <---> [MySQL Database]
```

- Frontend **Vue.js**
    - setup Vue project structure
    - users Verification
    - UI
    - improve users' experience
- Backend **Flask, Python**
    - setup Flask project structure
    - implement the register and login api using JWT or Flask-Login
    - tasks management api
    - database design using SQLAlchemy and Flask-Migrate
- Database **MySQL**
    - database models
    - data migration
- Implementation of the features
    - user register and login
    - creating and editing tasks
    - classification the tasks
    - deadline reminders
    - tasks priority
- Deployment
    - backend deployment using Docker to the server
    - frontend deployment using Netlify or Vercel
    - database deployment to AWS
- Project Description
    - project instruction
    - API

## Start the project (Windows 11)

### Backend (Flask, Python)

#### 1. Make sure you have installed Python and MySQL
#### 2. Setup the virtual environment and related packages
```bash
python -m venv venv
venv\Scripts\activate
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended
```
#### 3. Create the project structure for Flask
```plaintext
MyToDoList/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── config.py
├── migrations/
├── venv/
└── run.py
```
#### 4. Initialize the Flask App

- `run.py`
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```
- `app/__init__.py`
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    return app
```
- `app/config.py` Enter the username, password, and Database name of MySQL. 
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://<username/root>:<password>@localhost/<databasename/todo_app>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
- `app/models.py`
```python
from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(64), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```
- `app/routes.py`
```python
from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return "Hello, World!"
```
- execute `flask db init` in the terminal

- create a Database in MySQL
    - open MySQL command line client
    - `CREATE DATABASE todo_app;`
- execute `flask db migrate -m "Initial migration"` in the terminal
- execute `flask db upgrade` in the terminal
- test api by execute `flask run` in the terminal
- Open `http://127.0.0.1:5000/`