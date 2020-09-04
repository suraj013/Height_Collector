from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import  func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:suraj013@localhost/height_collector'
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://jdksalfxpyqlbo:4f1e1f87df822fee6c12003f012ccad60fef8ab9202d2d7204b3fa16945db94a@ec2-54-243-67-199.compute-1.amazonaws.com:5432/d2qlm52cotjovc?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://nwhzfnmvctaejh:7b0bc42217d0aed6551504a726d6e59d4e6bc79e5cd45f13ef46798d4b6fc915@ec2-107-20-15-85.compute-1.amazonaws.com:5432/dc2vih9f0sev7i?sslmode=require'

db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self,email_,height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form["email_name"]
        height=request.form["height_name"]
        #print(request.form)
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height,2)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template("success.html")
    return render_template("index.html",
    text="Seems like we have already got something from that Email Address!")


if __name__ == '__main__':
    app.debug=True
    app.run()