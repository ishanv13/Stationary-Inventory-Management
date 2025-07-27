import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Extensions

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_CONFIG', 'config.DevelopmentConfig'))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes.auth import auth_bp
    from .routes.inventory import inventory_bp
    from .routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(dashboard_bp)

    return app 