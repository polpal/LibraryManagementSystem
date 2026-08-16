from flask import Flask
from config import Config
from .models import db


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.main_routes import main_bp
    from .routes.member_routes import member_bp
    from .routes.book_routes import book_bp
    from .routes.transaction_routes import transaction_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(transaction_bp)
    

    return app