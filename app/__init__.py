from flask import Flask
from config import Config
from .models import db
from flask_wtf import CSRFProtect
from app.utils.logger import logger
from flask_login import LoginManager
from flask_migrate import Migrate
csrf = CSRFProtect()
login_manager = LoginManager()
from .models import User
from .routes.auth_routes import auth_bp
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    logger.info(
        "Application started"
    )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .routes.main_routes import main_bp
    from .routes.member_routes import member_bp
    from .routes.book_routes import book_bp
    from .routes.transaction_routes import transaction_bp
    from .routes.admin import admin_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.user_routes import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)

    return app