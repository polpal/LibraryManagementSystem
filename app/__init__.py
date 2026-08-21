from flask import Flask
from config import Config
from .models import db
from flask_wtf import CSRFProtect
from app.utils.logger import logger
csrf = CSRFProtect()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    logger.info(
        "Application started"
    )

    db.init_app(app)
    csrf.init_app(app)

    from .routes.main_routes import main_bp
    from .routes.member_routes import member_bp
    from .routes.book_routes import book_bp
    from .routes.transaction_routes import transaction_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(transaction_bp)
    

    return app