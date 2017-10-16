from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
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

    def __init__(self, username):
        self.username = username

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, symbol, user_id):
        self.symbol = symbol
        self.user_id = user_id

class Stock_Data(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    stock_price = db.Column(db.Float, nullable=False)
    quote_time = db.Column(db.String(10), nullable=False)
    prev_close = db.Column(db.Float, nullable=False)
    stock_name = db.Column(db.String(20), nullable=False)
    year_high = db.Column(db.Float, nullable=False)
    year_low = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.String(10), nullable=False)
    percent_change = db.Column(db.String(10), nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)

    def __init__(self, stock_price, quote_time, prev_close, stock_name, year_high, year_low, market_cap, percent_change, stock_id):
        self.stock_price = stock_price
        self.quote_time = quote_time
        self.prev_close = prev_close
        self.stock_name = stock_name
        self.year_high = year_high
        self.year_low = year_low
        self.market_cap = market_cap
        self.percent_change = percent_change
        self.stock_id = stock_id

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
            return render_template('login.html', error=error)
        else:
            user = User.query.filter_by(username=username).first()
            if User.query.filter_by(username=username).first():
                session['logged_in'] = True
                session['username'] = username
                # flash('Welcome back, ' + username + '!')
                return redirect(url_for('home'))
            else:
                user = User(username)
                db.session.add(user)
                db.session.commit()
                session['logged_in'] = True
                session['username'] = username
                # flash('You were successfully logged in!')
                return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    return redirect(url_for('login'))
    # remove the username from the session if it's there

@app.route('/home', methods=['GET'])
def home():
    if request.method == 'GET':
        stock_dict = {}
        stock_list = []
        current_user = User.query.filter_by(username=session['username']).first()
        user_id = current_user.id
        stocks = Stock.query.filter_by(user_id=user_id).all()
        if stocks == []:
            no_stocks = 'No saved stocks yet.'
            return render_template('home.html', current_user=current_user.username, no_stocks=no_stocks)
        else:
            for stock in stocks:
                symbol = stock.symbol
                stock_id = stock.id
                data = Stock_Data.query.filter_by(stock_id=stock_id).first()
                price = float("{0:.2f}".format(data.stock_price))
                time = data.quote_time
                prev = float("{0:.2f}".format(data.prev_close))
                change = float("{0:.2f}".format(price - prev))
                name = data.stock_name
                high = float("{0:.2f}".format(data.year_high))
                low = float("{0:.2f}".format(data.year_low))
                cap = data.market_cap
                percent = data.percent_change                
                stock_dict.update({'symbol':symbol, 'price':'$'+str(price), 'time':time, 'change':'$'+str(change), 'name':name, 'high':'$'+str(high), 'low':'$'+str(low), 'cap':'$'+str(cap), 'percent':percent})
                stock_list.append(stock_dict)
                stock_dict = {}
            return render_template('home.html', current_user=current_user.username, stock_list=stock_list)

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        request.get_data()
        data = request.json
        current_user = User.query.filter_by(username=session['username']).first()
        user_id = current_user.id
        stock_to_update = Stock.query.filter_by(user_id=user_id, symbol=data['symbol']).first()
        stock_id = stock_to_update.id
        stock_data_to_update = Stock_Data.query.filter_by(stock_id=stock_id).first()
        stock_data_to_update.stock_price = data['LastTradePriceOnly']
        stock_data_to_update.quote_time = data['LastTradeDate'] + ' at ' + data['LastTradeTime']
        stock_data_to_update.prev_close = data['PreviousClose']
        db.session.commit()
        return json.dumps(data)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        error = None
        request.get_data()
        data = request.json
        current_user = User.query.filter_by(username=session['username']).first()
        user_id = current_user.id
        symbol = data['symbol']
        price = data['LastTradePriceOnly']
        time = data['LastTradeDate'] + ' at ' + data['LastTradeTime']
        prev = data['PreviousClose']
        name = data['Name']
        high = data['YearHigh']
        low = data['YearLow']
        cap = data['MarketCapitalization']
        percent = data['ChangeinPercent']
        db.session.add(Stock(symbol, user_id))
        db.session.commit()
        stock = Stock.query.filter_by(symbol=symbol, user_id=user_id).first()
        db.session.add(Stock_Data(price, time, prev, name, high, low, cap, percent, stock.id))
        db.session.commit()
        return json.dumps(data)
    if request.method == 'GET':
        stock_dict = {}
        stock_list = []
        current_user = User.query.filter_by(username=session['username']).first()
        user_id = current_user.id
        stocks = Stock.query.filter_by(user_id=user_id).all()
        for stock in stocks:
            symbol = stock.symbol
            stock_id = stock.id
            data = Stock_Data.query.filter_by(stock_id=stock_id).first()
            price = float("{0:.2f}".format(data.stock_price))
            time = data.quote_time
            prev = float("{0:.2f}".format(data.prev_close))
            change = float("{0:.2f}".format(price - prev))
            name = data.stock_name
            high = float("{0:.2f}".format(data.year_high))
            low = float("{0:.2f}".format(data.year_low))
            cap = data.market_cap
            percent = data.percent_change
            stock_dict.update({'symbol':symbol, 'price':'$'+str(price), 'time':time, 'change':'$'+str(change), 'name':name, 'high':'$'+str(high), 'low':'$'+str(low), 'cap':'$'+str(cap), 'percent':percent})
            stock_list.append(stock_dict)
            stock_dict = {}
        return json.dumps(stock_list)

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        error = None
        request.get_data()
        symbol = request.json
        stock = db.session.query(Stock).filter_by(symbol=symbol).first()
        db.session.delete(stock)
        stock_data = Stock_Data.query.filter_by(stock_id=stock.id).first()
        db.session.delete(stock_data)
        db.session.commit()
        # return redirect(url_for('home'))
        return json.dumps(symbol)

# db.drop_all()
db.create_all()
db.session.commit()

if __name__ == '__main__':
     app.run()
