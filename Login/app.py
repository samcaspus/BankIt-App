from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Login(db.Model): 
    uid = db.Column(db.Integer(), primary_key=True) 
    passw = db.Column(db.String(45), nullable=False) 
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __init__(self, uid, passw):
    self.uid = uid
    self.passw = passw
    self.datetime = datetime

def __repr__(self): 
    return "Cashier id: "+str(self.uid)



@app.route('/') 
def home(): 
    return render_template('index.html')  

@app.route('/login', methods=['POST']) 
def login():   
    if request.method == 'POST':
        if 'uid' in request.form:
            uid = int(request.form['uid'])  
            passw = str(request.form['passw'])
            results = db.session.query(Login).filter(Login.uid==uid)
            x = [print(i) for i in results]
            if len(x) == 0:
                return render_template('error.html')
            else:  
                for row in results:
                    if (row.uid == uid) and (row.passw == passw):
                        return render_template('login.html')
                return render_template('index.html')
    else:
        return render_template('index.html')     
if __name__ == '__main__':
    app.run(debug=True)
