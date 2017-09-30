from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

app = Flask(__name__)
app.config.update(
DEBUG = True,
SQLALCHEMY_TRACK_MODIFICATIONS = False,
SQLALCHEMY_DATABASE_URI = 'sqlite:///stock_ticker.db',
SECRET_KEY = 'foryoureyesonly'
)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    stocks = db.relationship('User_Stock', backref='user', lazy=True)

    def __init__(self, username, stocks):
        self.username = username
        self.stocks = stocks

    def __repr__(self):
        return '<User %r>' % self.username

class User_Stock(db.Model):
    __tablename__ = 'user_stock'
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    stock_data = db.relationship('Stock_Data', backref='user_stock', lazy=True)

    # user = relationship("User", back_populates="stocks")

    def __repr__(self):
        return "<User_Stock(stock='%s')>" % self.stock

class Stock_Data(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    stock_price = db.Column(db.String(10), nullable=False)
    quote_time = db.Column(db.String(10), nullable=False)
    user_stock_id = db.Column(db.Integer, db.ForeignKey('user_stock.id'),
        nullable=False)

    def __repr__(self):
        return "<Stock_Data(data='%s')>" % self.price

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = ''.join(request.form.getlist('username'))
        if username == '':
            error = 'Please enter a username.'
            # return login()
        else:
            user = User.query.filter_by(username=username).first()
            if User.query.filter_by(username=username).first():
                session['logged_in'] = True
                session['username'] = username
                # session['user_id'] = username
                flash('Welcome back, ' + username + '!')
                return redirect(url_for('home'))
            else:
                user = User(username, [])
                db.session.add(user)
                db.session.commit()
                session['logged_in'] = True
                flash('You were successfully logged in!')
                return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()
    # remove the username from the session if it's there
    # session.pop('username', None)
    # return redirect(url_for('login'))

@app.route('/home', methods=['GET'])
def home():
    current_user = User.query.filter_by(username=session['username']).first()
    return render_template('home.html', current_user=current_user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    request.get_data()
    data = request.json
    print('symbol: ', data.symbol)
    print('symbol: ', data.LastTradePriceOnly)
    print('symbol: ', data.LastTradeDate + " at " + data.LastTradeTime)

    return json.dumps(data)
    # ({'symbol': data.symbol,'quote': data.quote})

if __name__ == '__main__':
     app.run()
