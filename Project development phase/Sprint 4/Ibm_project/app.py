from flask import Flask, render_template,url_for,redirect,request,session
from werkzeug.utils import secure_filename
from importlib.resources import contents
from tkinter import S
from turtle import title
from flask import Flask,redirect, render_template, request, session, url_for,flash
from pyexpat import model
from sqlalchemy import PrimaryKeyConstraint
from werkzeug.utils import secure_filename

from markupsafe import escape
import os

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=csr80916;PWD=yUE8PuQT3mYrvp9N",'','')
print(conn)
print("Login sucessful")

app = Flask(__name__)
app.secret_key = '32y[wld,fnpsygfwfpwek2;]1[2'

@app.route('/')
def home():
    message = "TEAM ID : PNT2022TMID29859" +" "+ "BATCH ID : B1-1M3E "
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('coding_based.html')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    return render_template('register.html')

@app.route('/studentdashboard', methods = ['GET','POST'])
def studentdashboard():
    return render_template('Stdash.html')

@app.route('/industrydashboard', methods = ['GET','POST'])
def industrydashboard():
    return render_template('Indusdash.html')

@app.route('/changepass', methods = ['GET','POST'])
def changepass():
    return render_template('changepass.html')

@app.route('/register_industry', methods=['GET', 'POST'])
def register_industry():
    if request.method == 'POST':
        name = request.form['Nm']
        email = request.form['email']
        phonenumber = request.form['PhNo']
        password = request.form['pass']
            
        sql = "SELECT * FROM industry WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            flash("Record Aldready found", "success")
        
        else:
            insert_sql = "insert into industry(name,email,phonenumber,password)values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phonenumber)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            return redirect(url_for("login"))

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form["Nm"]
        email = request.form["email"]
        phonenumber = request.form['PhNo']
        password = request.form['pass']
            
        sql = "SELECT * FROM student1 WHERE email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            flash("Record Aldready found", "success")
        
        else:
            insert_sql = "insert into student1(name,email,phonenumber,password)values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phonenumber)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            return redirect(url_for('login'))

@app.route('/login_industry', methods=['GET', 'POST'])
def login_industry():
    if request.method == 'POST':
        mail = request.form['em']
        password = request.form['pass']
        print(id, password)
        sql = f"select * from industry where email='{escape(mail)}' and password='{escape(password)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)
            
        if data:
            session["mail"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for("industrydashboard"))

        else:
            return redirect(url_for("login",msg = "Account does not exits or invalid"))
    else:
        return "NOT WORKING"

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        mail = request.form["em"]
        password = request.form["pass"]
        sql = f"select * from student1 where email='{escape(mail)}' and password='{escape(password)}'"
        stmt = ibm_db.exec_immediate(conn, sql)
        data = ibm_db.fetch_both(stmt)
            
        if data:
            session["em"] = escape(mail)
            session["password"] = escape(password)
            return redirect(url_for("studentdashboard"))

        else:
            return redirect(url_for("login",msg = "Account does not exits or invalid"))

    else:
        return "NOT WORKING"




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)