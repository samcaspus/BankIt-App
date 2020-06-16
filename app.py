from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy import and_


# ###########################
# Database Configuration
# 
# Note: Kindly make sure the status is any one of the following: Active, Closed, Pending <Some Activity> 
# ###########################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cid = db.Column(db.Integer(), nullable=False)
    ssnid = db.Column(db.Integer(), nullable=False)
    accountId = db.Column(db.Integer(), nullable=False)
    accountBalance = db.Column(db.Integer(), nullable=False)
    account_type = db.Column(db.String(1), nullable=False)
    status = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)


    def __init__(self, cid, ssnid, accountId, accountBalance, account_type, status, message):
        self.cid = cid
        self.ssnid = ssnid
        self.accountId = accountId
        self.accountBalance = accountBalance
        self.account_type = account_type
        self.status = status
        self.message = message
        

    def __repr__(self):
        return "Customer id: "+str(self.cid)

# ###########################
# Initializing Dummy Data (Run in Python Terminal)
# ###########################

# from app import db
# from app import Customer
# db.create_all()

# db.session.add(Customer(cid=123456789, ssnid=518612602, accountId=553794213, accountBalance=10000, account_type='S', status='Pending Approval', message='Just Created'))
# db.session.add(Customer(cid=888888888, ssnid=372781404, accountId=310556749, accountBalance=2000, account_type='C', status='Active', message='Nothing'))
# db.session.add(Customer(cid=999999999, ssnid=177513079, accountId=500864310, accountBalance=500000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(cid=777777777, ssnid=196751448, accountId=546723186, accountBalance=1000000, account_type='S', status='Pending Approval', message='NA'))
# db.session.add(Customer(cid=666666666, ssnid=388288542, accountId=620951719, accountBalance=10, account_type='C', status='Closed', message='Closed due to low balance'))
# db.session.add(Customer(cid=777777777, ssnid=196751448, accountId=546723186, accountBalance=500, account_type='C', status='Active', message='Secondary Account of Type Current'))

# db.session.commit()

# ###########################
# Routing
# ###########################

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/CustomerStatus')
def CustomerStatus():
    all_customer = Customer.query.all()
    return render_template('customer-Status.html', rows=all_customer)

@app.route('/AccountStatus')
def AccountStatus():
    all_account = Customer.query.all()
    return render_template('account-Status.html', rows=all_account)

@app.route('/CustomerSearch', methods=['GET', 'POST'])
def CustomerSearch():
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.cid == cid)
            return render_template('customer-Search.html', result=results)
        else:
            ssnid = request.form['ssnid']
            results = db.session.query(Customer).filter(Customer.ssnid == ssnid)
            return render_template('customer-Search.html', result=results)
    else:   
        return render_template('customer-Search.html')

@app.route('/AccountSearch', methods=['GET', 'POST'])
def AccountSearch():
    if request.method == 'POST':
       
        if 'accid' in request.form:
            accid = request.form['accid']
            results = db.session.query(Customer).filter(Customer.accountId == accid)
            return render_template('account-Search.html', result=results)
        else:
            cid = request.form['cid']
            results = db.session.query(Customer).filter(Customer.cid == cid)
            return render_template('account-Search.html', result=results)
    else:   
        return render_template('account-Search.html')

@app.route('/Deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        accid = request.form['accid']
        results = db.session.query(Customer).filter(Customer.accountId == accid)
        return render_template('Deposit.html',result=results)

@app.route("/update", methods=["POST",'GET'])
def update():
    if request.method == 'POST':
        newb = request.form["dep"]
        oldb = request.form["oldbalance"]
        accid=request.form["accid"]
        cust = Customer.query.filter_by(accountId=accid).first()
        cust.accountBalance = (int)(oldb)+(int)(newb)
        cust.message="Deposit success"
        db.session.commit()
        return redirect("/AccountStatus")

@app.route("/withdrawupdate", methods=["POST",'GET'])
def withdrawupdate():
    if request.method == 'POST':
        newb = request.form["dep"]
        oldb = request.form["oldbalance"]
        accid=request.form["accid"]
        cust = Customer.query.filter_by(accountId=accid).first()
        if((int)(oldb)-(int)(newb) < 0):
            cust.message="Withdraw failed"
        else:
            cust.accountBalance = (int)(oldb)-(int)(newb)
            cust.message="Withdraw success"
        db.session.commit()
        return redirect("/AccountStatus")




@app.route('/Withdraw',methods=["POST",'GET'])
def withdraw():
    if request.method == 'POST':
        accid = request.form['accid']
        results = db.session.query(Customer).filter(Customer.accountId == accid)
        return render_template('withdraw.html',result=results)


@app.route('/Transfer',methods=["POST",'GET'])
def transfer():
    if request.method == 'POST':
        accid = request.form['accid']
        results = db.session.query(Customer).filter(Customer.accountId == accid)
        return render_template('transfer.html',result=results)

@app.route("/transferupdate", methods=["POST",'GET'])
def transferupdate():
    if request.method == 'POST':
        tran = request.form["dep"]
        stype = request.form["stype"]
        ttype=request.form["ttype"]
        accid=request.form["accid"]
        scust = db.session.query(Customer).filter(and_(Customer.cid == accid,Customer.account_type==stype[0])).first()
        tcust = db.session.query(Customer).filter(and_(Customer.cid==accid,Customer.account_type==ttype[0])).first()
        
        if(stype==ttype):

            scust.message="Transfer failed"

        elif(int(scust.accountBalance)-int(tran) < 0 ):
            
            scust.message="Insufficient balance for transfer"
        else:
            scust.accountBalance = int(scust.accountBalance)-int(tran)
            tcust.accountBalance = int(tcust.accountBalance)+int(tran)
            scust.message="Transfer success"
            tcust.message="Money Recieved"
            
        db.session.commit()
        return redirect("/AccountStatus")

@app.route("/transferupdates", methods=["POST",'GET'])
def transferupdates():
    if request.method == 'POST':
        tran = request.form["tran"]
        tacc=request.form["tacc"]
        accid=request.form["accid"]
        scust = db.session.query(Customer).filter(Customer.accountId == accid).first()
        tcust = db.session.query(Customer).filter(Customer.accountId == tacc).first()
        
        if(accid == tacc):

            scust.message="Transfer failed because source and target accounts are same."
        if(scust is None or tcust is None):
            scust.message="Transfer failed.Check Account IDs"
        elif(int(scust.accountBalance)-int(tran) < 0 ):
            
            scust.message="Insufficient balance for transfer"
        else:
            scust.accountBalance = int(scust.accountBalance)-int(tran)
            tcust.accountBalance = int(tcust.accountBalance)+int(tran)
            scust.message="Transfer success"
            tcust.message="Money Recieved"
            
        db.session.commit()
        return redirect("/AccountStatus")

if __name__ == '__main__':
    app.run(debug=True)
