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
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    #create func to return string when we create a entry
    def __repr__(self):
        return '<Name %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/userlist', methods = ['POST', 'GET'])
def userlist():
    if request.method == "POST":
        username = request.form["username"]
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

'''@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name = user))'''
if __name__ == '__main__':
    app.run(debug = True)