from flask import Flask , request,redirect, session, url_for, flash
from flask import render_template
import mysql.connector
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField,BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_mysqldb import MySQL
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask
app = Flask(__name__)
app = Flask(__name__)
Bootstrap(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '23234455'
app.config['MYSQL_DB'] = 'zrdata'
Mysql = MySQL(app)

conn =  mysql.connector.connect(host='localhost',
                                         database='zrdata',
                                         user='root',
                                         password='23234455',
                                         port='3306')
cursor = conn.cursor()
app.secret_key=os.urandom(24)

@app.route('/')
def login():

    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

# curs = Mysql.connection.cursor()
# @app.route('/home')
# def count():
#     cur = Mysql.connection.cursor()
#     cur.execute('SELECT sum(fund) from family')
#     datas=cur.fetchall()
#     database = str(datas)
#     render_template("home.html")

@app.route('/home')
def home():
    if 'user_id' in session:

        cur = Mysql.connection.cursor()
        cur.execute('SELECT * FROM family')
        data = cur.fetchall()
        cur.execute('SELECT sum(fund) from family')
        test = cur.fetchall()


        cur.execute('SELECT * FROM users')
        users=cur.fetchall()

    # curs=Mysql.connection.cursor()
    # curs.execute('INSERT INTO test (names) SELECT count(*) FROM family')

        numbers=len(data)
        for datas in test:
            if len(datas)>0:
                funds=int(''.join(map(str,datas)))
                print("all sum of funds:",funds)
            else:
                funds = 0
        leng=len(users)
        print("user total ",leng)
    # datas=curs.fetchall()
    # cur.close()
        return render_template("home.html",contacts = data,num=numbers,funds=funds,total = leng)
    else:
        return redirect('/')
@app.route('/login_validation',methods=['POST'])
def login_validation():
    email= request.form.get('email')
    password= request.form.get('password')
    cursor.execute("""SELECT * FROM `users` where `email` LIKE '{}' AND `password` LIKE '{}'"""
    .format(email,password))
    users=cursor.fetchall()
    # cursor.execute("""insert into test (names) select count(*) from family""")
    # datas= cursor.fetchall()
    if email == "anonim5284@gmail.com" and password == "z.rfoundation":
        flash('Contact Updated Successfully')
        return redirect('/index')    
    elif len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')



@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    password = request.form.get('upass')
    email = request.form.get('uemail')

    cursor.execute("""INSERT INTO `users` (`idu`,`username`,`email`,`password`) VALUES (NULL,'{}','{}','{}')"""
    .format(name,email,password))
    conn.commit()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/index')
def Index():
    cur = Mysql.connection.cursor()
    cur.execute('SELECT * FROM family')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        member = request.form['member']
        address = request.form['address']
        fund = request.form['fund']
        curss = Mysql.connection.cursor()
        curss.execute("INSERT INTO family (name,member,location, fund) VALUES (%s,%s,%s,%s)", (fullname, member, address,fund))
        Mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cursex = Mysql.connection.cursor()
    cursex.execute('SELECT * FROM family WHERE idf = %s', (id))
    data = cursex.fetchall()
    cursex.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        member = request.form['memeber']
        address = request.form['address']
        fund = request.form['fund']
        cursef = Mysql.connection.cursor()
        cursef.execute("""
            UPDATE family
            SET name = %s,
                member = %s,
                location = %s,
                fund = %s
            WHERE idf = %s
        """, (fullname, member, address,fund, id))
        flash('Contact Updated Successfully')
        Mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    curser = Mysql.connection.cursor()
    curser.execute('DELETE FROM family WHERE idf = {0}'.format(id))
    Mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port='4333',debug=True)
