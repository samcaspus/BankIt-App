from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cid_generator import randN
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


class CustomerDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cid = db.Column(db.Integer(), nullable=False)
    ssnid = db.Column(db.Integer(), nullable=False)
    customer_name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(10), nullable=False)

    def __init__(self, cid, ssnid, customer_name, age, address, state, city):
        self.cid = cid
        self.ssnid = ssnid
        self.customer_name = customer_name
        self.age = age
        self.address = address
        self.state = state
        self.city = city

    def __repr__(self):
        return "Customer Detail id: "+str(self.cid)


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cid = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    source_acc_type = db.Column(db.String(1), nullable=False)
    target_acc_type = db.Column(db.String(1), nullable=False)
    tans_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    trans_type = db.Column(db.String(1), nullable=False)

    def __init__(self, cid, amount, source_acc_type, target_acc_type, trans_type):
        self.cid = cid
        self.amount = amount
        self.source_acc_type = source_acc_type
        self.target_acc_type = target_acc_type
        self.trans_type = trans_type
        
    def __repr__(self):
        return "Transaction id: "+str(self.id)

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
        db.session.add(Transaction(cid=cust.cid, amount=(int)(newb), source_acc_type=cust.account_type, target_acc_type=cust.account_type, trans_type='C'))
        cust.message="Amount Deposited Successfully."
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
            cust.message="Withdraw Failed Due to Low Balance."
        else:
            cust.accountBalance = (int)(oldb)-(int)(newb)
            db.session.add(Transaction(cid=cust.cid, amount=(int)(newb), source_acc_type=cust.account_type, target_acc_type=cust.account_type, trans_type='D'))
            cust.message="Amount Withdrawn Successfully."
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
            scust.message="Transfer Successful."
            db.session.add(Transaction(cid=scust.cid, amount=(int)(tran), source_acc_type=scust.account_type, target_acc_type=tcust.account_type, trans_type='D'))
            tcust.message="Transfer Successful, Money Recieved."
            db.session.add(Transaction(cid=tcust.cid, amount=(int)(tran), source_acc_type=scust.account_type, target_acc_type=tcust.account_type, trans_type='C'))
            
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
            scust.message="Transfer failed. Check Account IDs"
        elif(int(scust.accountBalance)-int(tran) < 0 ):
            
            scust.message="Insufficient balance for transfer"
        else:
            scust.accountBalance = int(scust.accountBalance)-int(tran)
            tcust.accountBalance = int(tcust.accountBalance)+int(tran)
            scust.message="Transfer Successful"
            db.session.add(Transaction(cid=scust.cid, amount=(int)(tran), source_acc_type=scust.account_type, target_acc_type=tcust.account_type, trans_type='D'))
            tcust.message="Transfer Successful, Money Recieved."
            db.session.add(Transaction(cid=tcust.cid, amount=(int)(tran), source_acc_type=scust.account_type, target_acc_type=tcust.account_type, trans_type='C'))
        db.session.commit()
        return redirect("/AccountStatus")

@app.route("/AccountStatement", methods=["POST",'GET'])
def AccountStatement():
    if request.method == 'POST':
        if request.form['option'] == 'trans':
            n = request.form['number']
            if (int)(n) > 0:
                accid = request.form['accid']
                c = db.session.query(Customer).filter(Customer.accountId == accid).count()
                if c == 0:
                    return render_template('account-Statement.html', error="No Account was found.")
                else:
                    customer = db.session.query(Customer).filter(Customer.accountId == accid).all()[0].cid
                    transaction = db.session.query(Transaction).filter(Transaction.cid == customer).limit(n)
                    return render_template('account-Statement.html', transaction=transaction)
            else:
                return render_template('account-Statement.html', error="Please Select Number of Transactions")
        elif request.form['option'] == 'dates':
            sd = request.form['startdate']
            ed = request.form['enddate']
            sd = datetime.strptime((sd + " 00:00:00"), '%Y-%m-%d %H:%M:%S')
            ed = datetime.strptime((ed + " 00:00:00"), '%Y-%m-%d %H:%M:%S')
            if sd > ed:
                return render_template('account-Statement.html', error="Invalid Date was found.")
            else:
                accid = request.form['accid']
                c = db.session.query(Customer).filter(Customer.accountId == accid).count()
                if c == 0:
                    return render_template('account-Statement.html', error="No Account was found.")
                else:
                    customer = db.session.query(Customer).filter(Customer.accountId == accid).all()[0].cid
                    transaction = db.session.query(Transaction).filter(Transaction.cid == customer).filter(Transaction.tans_date >= sd).filter(Transaction.tans_date <= ed)
                    return render_template('account-Statement.html', transaction=transaction)
        else:
            return render_template('account-Statement.html', error="Invalid Input was found.")

    else:
        return render_template('account-Statement.html')


@app.route('/createcustomer', methods=['GET', 'POST'])
def Createcustomer():
    cid = int(randN())
    print(cid)
    # rendered = render_template('create-customer.html', cid=cid) 
    if request.method == 'POST':
        if 'ssnid' in request.form:
            ssnid = int(request.form['ssnid'])
            customer_name = request.form['customer_name']
            age = int(request.form['age'])
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            
            # inserting data
            db.create_all()
            db.session.add(CustomerDetails(cid=cid, ssnid=ssnid, customer_name=customer_name, age=age, address=address, state=state, city=city))
            db.session.commit()
            return render_template('create-customer.html')
        else:
            return render_template('create-customer.html') 
    else:
        return render_template('error.html') 


@app.route('/addaccount', methods =['GET','POST'])
def Addaccount():  
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            account_type = request.form['account_type']
            accountBalance = request.form['accountBalance']

            results = db.session.query(CustomerDetails).filter(CustomerDetails.cid==cid)
            x = [print(i) for i in results]
            if len(x) == 0:
                return render_template('error.html')
            else:
                for row in results:
                    ssnid = row.ssnid
                accountId = int(randN())
                db.session.add(Customer(cid=cid, ssnid=ssnid, accountId=accountId, accountBalance=accountBalance, account_type=account_type, status='Pending Approval', message='Just Created'))
                db.session.commit()
                return render_template('create-account.html')
        else:
            return render_template('create-account.html')
    else:
        return render_template('create-account.html') 

@app.route('/updatecustomer', methods =['GET','POST'])
def UpdateCustomer(): 
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            customer_name = request.form['customer_name']
            address = request.form['address']
            age = int(request.form['age'])

            results = db.session.query(CustomerDetails).filter(CustomerDetails.cid == cid)
            x = [print(i) for i in results]
            
            if len(x) == 0:
                return render_template('error.html')
            else:
                for row in results:
                    row.customer_name = customer_name
                    row.address = address
                    row.age = age
                    db.session.commit()
                return render_template('update-customer.html')
        else:
            return render_template('update-customer.html')
    else:
        return render_template('update-customer.html')


@app.route('/deletecustomer', methods =['GET','POST'])
def DeleteCustomer(): 
    if request.method == 'POST':
        if 'cid' in request.form:
            cid = int(request.form['cid'])
            results = db.session.query(CustomerDetails).filter(CustomerDetails.cid == cid)
            x = [print(i) for i in results]
            if len(x) == 0:
                return render_template('error.html')
            else:
                db.session.query(Customer).filter(Customer.cid == cid).delete()
                db.session.query(CustomerDetails).filter(CustomerDetails.cid == cid).delete()
                db.session.commit()
                return render_template('delete-customer.html')
        else:
            return render_template('delete-customer.html')
    else:
        return render_template('delete-customer.html')

@app.route('/deleteaccount', methods =['GET','POST'])
def DeleteAccount(): 
    if request.method == 'POST':
        if 'accountId' in request.form:
            accountId = int(request.form['accountId'])
            results = db.session.query(Customer).filter(Customer.accountId == accountId)
            x = [print(i) for i in results]
            if len(x) == 0:
                return render_template('error.html')
            else:
                db.session.query(Customer).filter(Customer.accountId == accountId).delete()
                db.session.commit()
                return render_template('delete-account.html')
        else:
            return render_template('delete-account.html')
    else:
        return render_template('delete-account.html')


if __name__ == '__main__':
    app.run(debug=True)