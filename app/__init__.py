from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.home import home_bp
    from app.routes.videos import videos_bp
    from app.routes.posts import posts_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(posts_bp)

    return app