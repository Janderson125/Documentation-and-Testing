from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mechanics.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress warning

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register your blueprints
    from app.routes.mechanics import mechanics_bp
    from app.routes.customers import customers_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(auth_bp)

    # Root route
    @app.route('/')
    def home():
        return "Welcome to the Mechanic API!"

    # Swagger UI setup
    swaggerui_blueprint = get_swaggerui_blueprint(
        '/swagger',
        '/static/swagger.yaml',
        config={'app_name': "Mechanic API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

    return app
