from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#! Register Blueprints from views folder
from views.user_routes import user_bp
from views.task_route import task_bp
from views.project_route import project_bp


app.register_blueprint(user_bp)
app.register_blueprint(task_bp)
app.register_blueprint(project_bp)

if __name__ == '__main__':
    app.run(debug=True)
