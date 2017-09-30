from flask import Flask, g, request, redirect, url_for, render_template
from app import app, db
from .models import User, Stock
# from flask_login import LoginManager, login_user, logout_user, login_required
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route('/')
def index():
    # if 'username' in session:
    #     return 'Logged in as %s' % escape(session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # if request.form['username'] != 'admin':
        # User.query.filter(User.username==username)
        # print(username)
            #create username if None
        # session['username'] = request.form['username']
        username = request.form.getlist('username')
        print('username: ', ''.join(username))
        user = User(str(username), [])
        print('user: ', user)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('app'))
    return render_template('login.html')
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    # return app.send_static_file('login.html', error=error)

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    # remove the username from the session if it's there
    # session.pop('username', None)
    # return redirect(url_for('login'))

@app.route('/app', methods=['GET'])
# @login_required
def app():
    # current_user = User.query.filter_by(username='peter').first()
    return render_template('stock_ticker.html')

#username query
# @app.route('/user/<username>/', methods=["GET"])
# def user(username):
#     User.query.filter(User.username==username)
#     if username is None:
#         return render_template("directory.html",username=username,contacts=contacts)

# @app.route('/app/username/search', methods=['GET', 'POST'])
#     def search():
