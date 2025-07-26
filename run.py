from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_folder='app/static')  # adjust if your static folder is elsewhere

SWAGGER_URL = '/swagger'  # URL to access Swagger UI
API_URL = '/static/swagger.yaml'  # path to your swagger.yaml file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def hello():
    return "Welcome to the Mechanic API!"

if __name__ == '__main__':
    app.run(debug=True)
