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
    stocks = db.relationship('Stock', backref='user', lazy=True)

    def __init__(self, username, stocks):
        self.username = username
        self.stocks = stocks

    # def __repr__(self):
    #     return '<User %r>' % self.username

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    stock_data = db.relationship('Stock_Data', backref='stock', lazy=True)

    # user = relationship("User", back_populates="stocks")
    def __init__(self, symbol, user_id, stock_data):
        self.symbol = symbol
        self.user_id = user_id
        self.stock_data = stock_data

    # def __repr__(self):
    #     return "<User_Stock(symbol='%s')>" % self.symbol

class Stock_Data(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    stock_price = db.Column(db.String(10), nullable=False)
    quote_time = db.Column(db.String(10), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'),
        nullable=False)

    def __init__(self, stock_price, quote_time, stock_id):
        self.stock_price = stock_price
        self.quote_time = quote_time
        self.stock_id = stock_id

    # def __repr__(self):
    #     return "<Stock_Data(data='%s')>" % self.price

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
                flash('Welcome back, ' + username + '!')
                return redirect(url_for('home'))
            else:
                user = User(username, [])
                db.session.add(user)
                db.session.commit()
                session['logged_in'] = True
                session['username'] = username
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
    current_user = User.query.filter_by(username=session['username']).first()
    print('symbol: ', data['symbol'])
    print('symbol: ', data['LastTradePriceOnly'])
    print('symbol: ', data['LastTradeDate'] + " at " + data['LastTradeTime'])
    print('USERNAME?? ', current_user.username)
    print('USER ID?? ', current_user.id)
    # db.session.add(User_Stock(data['symbol']), current_user.id)
    # db.session.add(Stock_Data(data['LastTradePriceOnly'], data['LastTradeTime']))
    # db.session.commit()
    # stock = Stock.query.filter_by(stock=data['symbol']).first()
    # print('STOCK?!? ', stock)

    return json.dumps(data)
    # ({'symbol': data.symbol,'quote': data.quote})

# db.drop_all()
db.create_all()
db.session.commit()

if __name__ == '__main__':
     app.run()
