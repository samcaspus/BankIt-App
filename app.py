from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class Customer:
    id = db.Column(db.Integer(), primary_key=True)
    ssnid = db.Column(db.Integer(), unique=True, nullable=False)
    accountId = db.Column(db.Integer(), nullable=False)
    account_type = db.Column(db.String(1), nullable=False)
    status = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, ssnid, accountId, account_type, status, last_updated):
        self.ssnid = ssnid
        self.accountId = accountId
        self.account_type = account_type
        self.status = status
        self.last_updated = last_updated

    def __repr__(self):
        return "Customer id: "+str(self.id)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
