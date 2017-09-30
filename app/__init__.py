from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db = SQLAlchemy()
#
# def create_app():
#   app = Flask(__name__)
app.config.update(
DEBUG = True,
SQLALCHEMY_TRACK_MODIFICATIONS = False,
SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/allengordon/Desktop/stock_ticker/app/stock_ticker.db'
)
#   db.init_app(app)
#   return app

db = SQLAlchemy(app)


from app import views, models
