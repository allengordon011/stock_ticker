# from sqlalchemy import Table, Column, Integer, String
# from sqlalchemy.orm import mapper
# from database import metadata, db_session
#
# class User(object):
#     query = db_session.query_property()
#
#     def __init__(self, name=None, email=None):
#         self.name = name
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)
#
# users = Table('users', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(50), unique=True),
#     # Column('email', String(120), unique=True)
# )
# mapper(User, users)

# class User(db.Model):
#     # __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     stocks = db.relationship('Stock', backref='user', lazy=True)
#
#     def __init__(self,username,stocks):
#         self.username = username
#         self.stocks = stocks
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# class Stock(db.Model):
#     # __tablename__ = 'stocks'
#     id = db.Column(db.Integer, primary_key=True)
#     stock = db.Column(db.String(60), nullable=False)
#     time = datetime.datetime.now
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
#         nullable=False)
#
#     # user = relationship("User", back_populates="stocks")
#
#     def __repr__(self):
#         return "<Stock(stock='%s')>" % self.stock
#
# db.create_all()

# User.stocks = relationship("Stock", order_by=Stock.id, back_populates="user")
