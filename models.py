from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users' 
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    projects = db.relationship('Project', backref='owner', lazy=True)
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)

    def set_password(self, password):
        """Set the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    __tablename__ = 'projects' 

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')  

    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'  

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  

    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
