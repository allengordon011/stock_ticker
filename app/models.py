# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app import db
import datetime

class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    stocks = db.relationship('Stock', backref='user', lazy=True)

    def __init__(self,username,stocks):
        self.username = username
        self.stocks = stocks

    def __repr__(self):
        return '<User %r>' % self.username

class Stock(db.Model):
    # __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(60), nullable=False)
    time = datetime.datetime.now
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    # user = relationship("User", back_populates="stocks")

    def __repr__(self):
        return "<Stock(stock='%s')>" % self.stock

db.create_all()

# User.stocks = relationship("Stock", order_by=Stock.id, back_populates="user")
