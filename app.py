from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#initialize a db
db = SQLAlchemy(app)

#create a db model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    fullname = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    #create func to return string when we create a entry
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def index():
    return render_template('register.html')

'''
@app.route('/userlist', methods = ['POST', 'GET'])
def userlist():
    if request.method == "POST":
        fullname = request.form["username"]
        password = request.form["password"]

        new_user = Users(username=username, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('userlist'))
        except:
            return "There was an error adding user"

    else:
        users = Users.query.order_by(Users.date_joined)

        return render_template('userlist.html', users = users)
'''

@app.route('/login')
def loginrender():
    return render_template('login.html')


@app.route('/register')
def registerrender():
    return render_template('register.html')


@app.route('/userlogon', methods = ['POST', 'GET'])
def loginuser():
    return render_template('login.html')

@app.route('/registerUser', methods = ['POST', 'GET'])
def registerUser():
    if request.method == 'POST':
        email = request.form['email']
        fullname = request.form['fullname']
        address = request.form['address']
        password = request.form['email']
        new_user = Users(email = email, fullname = fullname, address = address, password = password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for(login))
        except:
            return "There was an error adding user"
        
        return redirect(url_for('index', name = user))

if __name__ == '__main__':
    app.run(debug = True)