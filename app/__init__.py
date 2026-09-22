from flask import Flask
from config import Config
from .models import db
from .models import User, Menu, RoleMenu
from flask_wtf import CSRFProtect
from app.utils.logger import logger
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

csrf = CSRFProtect()
login_manager = LoginManager()
from .models import User
from .routes.auth_routes import auth_bp
from flask import session
from .extensions import mail

migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    logger.info("Application started")

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
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
    from .routes.profile_routes import profile_bp
    from app.routes.book_category_routes import book_category_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(book_category_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)

    @app.after_request
    def prevent_browser_cache(response):
        if current_user.is_authenticated:

            response.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, max-age=0"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response

    @app.before_request
    def make_session_permanent():

        session.permanent = True

    @app.context_processor
    def inject_user_menus():

        if current_user.is_authenticated:

            menus = (
                Menu.query.join(RoleMenu, Menu.id == RoleMenu.menu_id)
                .filter(RoleMenu.role_name == current_user.role, Menu.is_active == True)
                .order_by(Menu.display_order)
                .all()
            )

        else:
            menus = []

        return {"user_menus": menus}

    return app
