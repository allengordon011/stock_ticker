from flask import Flask, g, request, redirect, url_for, render_template, session, flash, abort
from app import app, db
# from app import User, Stock
from models_new import User

@app.route('/')
def index():
    return 'Hello Allen'
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
    # else:
    #     return redirect(url_for('app'))

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
            print(user)
            if User.query.filter_by(username=username).first():
                session['logged_in'] = True
                session['username'] = username
                # session['user_id'] = username
                flash('Welcome back, ' + username + '!')
                return redirect(url_for('app'))
            else:
                user = User(username, [])
                print('NEW USER: ', user)
                db.session.add(user)
                db.session.commit()
                session['logged_in'] = True
                flash('You were successfully logged in!')
                return redirect(url_for('app'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return index()
    # remove the username from the session if it's there
    # session.pop('username', None)
    # return redirect(url_for('login'))

@app.route('/app', methods=['GET'])
def app():
    # current_user = User.query.filter_by(username='peter').first()
    if 'username' in session:
        user = session['username']
        # print ('USER LOGGED IN: ', user, user_id)
        # Stock.query.filter_by(user_id=user_id)
    return render_template('stock_ticker.html')

if __name__ == '__main__':
     app.run()

#username query
# @app.route('/user/<username>/', methods=["GET"])
# def user(username):
#     User.query.filter(User.username==username)
#     if username is None:
#         return render_template("directory.html",username=username,contacts=contacts)

# @app.route('/app/username/search', methods=['GET', 'POST'])
#     def search():
