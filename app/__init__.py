from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  # ✅ Load models so tables are registered
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()  # ✅ Now this will work

    return app
