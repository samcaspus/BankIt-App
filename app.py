from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# class Customer:
#     id = db.Column(db.Integer(), primary_key=True)
#     ssnid = db.Column(db.Integer(), unique=True, nullable=False)
#     cname = db.Column(db.String(30), nullable=False)
#     cage = db.Column(db.Integer(), nullable=False)
#     caddress = db.Column(db.Text, nullable=False)
#     ccity = db.Column(db.Text, nullable=False)
#     cstate = db.Column(db.Text, nullable=False)

#     def __init__(self, ssnid, cname, cage, caddress, ccity, cstate):
#         self.ssnid = ssnid
#         self.cname = cname
#         self.cage = cage
#         self.caddress = caddress
#         self.ccity = ccity
#         self.cstate = cstate

#     def __repr__(self):
#         return "Customer id: "+str(self.id)+" with Customer name: "+self.cname


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
