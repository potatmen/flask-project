from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
app = Flask(__name__)
app.secret_key = 'flka;sgadlgflaasd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html',values = users.query.all())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, '')
            db.session.add(usr)
            db.session.commit()
        flash('You are successfully logged in!', 'info')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('You are already logged in!', 'info')
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()

            flash('Your email was saved!', 'info')
        else:
            if 'email' in session:
                email = session['email']
        return render_template('user.html')
    else:
        flash('You are not logged in')
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    flash('You have been logged out!', 'info')
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))
@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        found_user = users.query.filter_by(name=name,email=email).first()
        if not found_user is None:
            db.session.delete(found_user)
            db.session.commit()
            if 'user' in session:
                session.pop('user',None)
                session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return render_template('delete.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=False)
