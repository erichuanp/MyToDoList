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

#### 1. Make sure you have installed [Python](https://www.python.org/downloads/) and [MySQL](https://dev.mysql.com/downloads/installer/)
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

#### 5. Using Postman to test api

- `app/routes.py`
    ```python
    from flask import Blueprint, request, jsonify
    from . import db
    from .models import User, Task
    from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

    bp = Blueprint('routes', __name__)

    @bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        new_user = User(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201

    @bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({"message": "Invalid credentials"}), 401

    @bp.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify([task.to_dict() for task in tasks]), 200

    @bp.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        data = request.get_json()
        print("Received task data:", data)
        user_id = get_jwt_identity()
        print("Authenticated user ID:", user_id)
        new_task = Task(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            due_date=data['due_date'],
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.commit()
        print("Task created successfully")
        return jsonify(new_task.to_dict()), 201

    @bp.route('/tasks/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_task(id):
        data = request.get_json()
        task = Task.query.get_or_404(id)
        task.title = data['title']
        task.description = data['description']
        task.priority = data['priority']
        task.due_date = data['due_date']
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @bp.route('/tasks/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    ```
- Restart the flask by `flask run` in terminal
- Open MySQL command line client and `USE todo_app;`
- Download [Postman](https://www.postman.com/downloads/)
- In Postman, Ctrl+T to add new requests. 
- Test Register:
    1. Type: POST
    2. URL: http://127.0.0.1:5000/register
    3. Body: 
        ```json
        {
            "username": "testuser",
            "password": "testpassword"
        }
        ```
    4. Send
    5. `SELECT * FROM user;` in MySQL and the result would be:
        ```plaintext
        +----+----------+--------------+
        | id | username | password     |
        +----+----------+--------------+
        |  1 | testuser | testpassword |
        +----+----------+--------------+
        ```
- Test Login:
    1. Type: POST
    2. URL: http://127.0.0.1:5000/login
    3. Body: 
        ```json
        {
            "username": "testuser",
            "password": "testpassword"
        }
        ```
    4. Send
    5. It will return a token. Copy this **token**. 
- Test Create Tasks:
    1. Type: POST
    2. URL: http://127.0.0.1:5000/tasks
    3. Click Authorization and choose `Bearer Token`, paste the **token**. 
    3. Body: 
        ```json
        {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "High",
            "due_date": "2024-12-31T23:59:59"
        }
        ```
    5. Send
    6. `SELECT * FROM task;` in MySQL and the result would be:
        ```plaintext
        +----+-----------+---------------------+----------+---------------------+---------+
        | id | title     | description         | priority | due_date            | user_id |
        +----+-----------+---------------------+----------+---------------------+---------+
        |  1 | Test Task | This is a test task | High     | 2024-12-31 23:59:59 |       1 |
        +----+-----------+---------------------+----------+---------------------+---------+
        ```
- Test Check Tasks:
    1. Type: GET
    2. URL: http://127.0.0.1:5000/tasks
    3. Click Authorization and choose `Bearer Token`, paste the **token**. 
    4. Send
    5. It will return the task you just added. 
- Test Update Tasks:
    1. Type: PUT
    2. URL: http://127.0.0.1:5000/tasks/1
    3. Click Authorization and choose `Bearer Token`, paste the **token**. 
    4. Body: 
        ```json
        {
            "title": "Updated Task",
            "description": "This is an updated test task",
            "priority": "Medium",
            "due_date": "2024-12-25T23:59:59"
        }
        ```
    5. Send
    6. `SELECT * FROM task;` in MySQL and the result would be:
        ```plaintext
        +----+--------------+------------------------------+----------+---------------------+---------+
        | id | title        | description                  | priority | due_date            | user_id |
        +----+--------------+------------------------------+----------+---------------------+---------+
        |  1 | Updated Task | This is an updated test task | Medium   | 2024-12-25 23:59:59 |       1 |
        +----+--------------+------------------------------+----------+---------------------+---------+
        ```
- Test Delete Tasks:
    1. Type: DELETE
    2. URL: http://127.0.0.1:5000/tasks/1
    3. Click Authorization and choose `Bearer Token`, paste the **token**. 
    4. Send
    5. `SELECT * FROM task;` in MySQL and the result would be empty
#### 6. You are all done with the backend

### Frontend (Vue.js)

