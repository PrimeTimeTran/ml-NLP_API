from flask import Flask
from src.routes import register_routes
from src.model import Model

app = Flask(__name__)

model_instance = Model()

register_routes(app, model_instance)

if __name__ == '__main__':
    app.run(debug=True)
