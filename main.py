from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flaskext.mysql import MySQL
from flask_mail import *
from random import *
import pymysql
import pdfkit
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_pyfile('config.py')

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)
otp = randint(000000, 999999)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

app.secret_key = 'ashish'

mysql = MySQL()

mysql.init_app(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def pl_home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM slider")
    slider = cursor.fetchall()

    cursor.execute(
        "SELECT date AS Date, COUNT(id ) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE() ")
    total = cursor.fetchone()
    cursor.execute("SELECT total_slot FROM slots")
    sl = cursor.fetchone()
    

    return render_template("pl_home.html", total=total, sl=sl, slider=slider)

# -------------------------------Login----------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM user_login WHERE email = %s AND password = %s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'

# ----------------------------------Admin Login------------------------------------

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM admin_login WHERE email=%s AND password=%s', (email, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('admin_dashboard'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/password!'

# --------------------------Super Admin Login-------------------------------------
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor.execute(
                'SELECT * FROM super_admin_login WHERE email=%s AND password=%s', (email, password))
            account = cursor.fetchone()

            if account:
                session['loggedin'] = True
                session['email'] = account['email']
                return redirect(url_for('super_admin_dashboard'))
            else:
                msg = 'Incorrect email/password!'

# -------------middle_ware login-------------------

        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            # Create variables for easy access
            email = request.form['email']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor.execute(
                'SELECT * FROM middle_ware WHERE email=%s AND password=%s', (email, password))
            # Fetch one record and return result
            account = cursor.fetchone()

            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['email'] = account['email']
                # Redirect to home page
                # return 'Logged in successfully!'
                return redirect(url_for('middle_ware'))
            else:
                # Account doesnt exist or email/password incorrect
                msg = 'Incorrect email/password!'

    return render_template('login.html', msg=msg)

# http://localhost:5000/register - this will be the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...

    msg = ''

    # Check if "email", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'mobile' in request.form and 'password' in request.form:
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user_login WHERE email = %s', (email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists! Please log in'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template("register.html", msg=msg)
        elif len(password) <= 6 and re.match(r'[A-Za-z0-9^@]+', password):
            msg = 'password minimum 6 characters and must contain one upper case letter,special character and numbers!'
            return render_template("register.html", msg=msg)
        elif confirm_password != password:
            msg = "password doesn't match"
            return render_template("register.html", msg=msg)
        elif not email or not password or not name or not confirm_password:
            msg = 'Please fill out the form!'
            return render_template("register.html", msg=msg)
        else:

            mail.send_message('New message from HEALTH CARE' + email,
                              sender=email,
                              recipients=[params['gmail-user']],
                              body=name + "\n" + email
                              )
            ms = Message('otp', sender='username@gmail.com',
                         recipients=[email])
            ms.body = str(otp)
            mail.send(ms)
            cursor.execute('INSERT INTO user_login (name, email, mobile, password, confirm_password) VALUES (%s, %s, %s, %s, %s)',
                           (name, email, mobile, password, confirm_password))
            conn.commit()
            msg = 'Successfully registered. Login To Continue'
            return render_template('verify.html')

    return render_template("register.html", msg=msg)


@app.route('/verify', methods=["POST"])
def verify():
    msgg = ''
    user_otp = request.form['otp']
    if otp == int(user_otp):
        msgg = 'You have successfully registered!'
        return render_template('login.html', msgg=msgg)
    elif request.method == 'POST':
        msgg = 'OTP does not match'
        return render_template('verify.html', msgg=msgg)


@app.route('/forget_password1', methods=["GET", "POST"])
def forget_password1():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'name' in request.form:
        # Create variables for easy access
        email = request.form['email']
        name = request.form['name']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM user_login WHERE email = %s AND name = %s', (email, name))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['email'] = account['email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('forget_password2'))
        else:
            # Account doesnt exist or email/password incorrect
            msg = 'Incorrect email/name!'
    return render_template('forget_password1.html', msg=msg)


@app.route('/forget_password2', methods=['GET', 'POST'])
def forget_password2():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'password' in request.form and 'confirm_password' in request.form:

        password = request.form['password']
        confirm_password = request.form['confirm_password']
        cursor.execute(
            'SELECT * FROM user_login WHERE password = %s', (password))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = "Can't Use Previous 3 passwords"

        elif len(password) <= 6 and re.match(r'[A-Za-z0-9^@]+', password):
            msg = 'password minimum 6 characters and must contain one upper case letter,special character and numbers!'
            return render_template("forget_password2.html", msg=msg)
        elif confirm_password != password:
            msg = "password doesn't match"
            return render_template("forget_password2.html", msg=msg)
        elif not password or not confirm_password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('UPDATE user_login SET password=%s,confirm_password=%s WHERE email="' +
                           session["email"] + '" ', (password, confirm_password))
            conn.commit()

            return redirect('login')
    return render_template('forget_password2.html', msg=msg)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        " SELECT date AS Date, COUNT(id) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE();")
    admin = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM online_appointment WHERE date(date) = CURDATE();")
    pd = cursor.fetchall()
    cursor.execute("SELECT * FROM doctors")
    doc = cursor.fetchall()

    cursor.execute("SELECT * FROM employee")
    emp = cursor.fetchall()

    cursor.execute("SELECT COUNT(id) as no_of_emp FROM employee WHERE status='Available' ")
    emp_avl = cursor.fetchone()

    cursor.execute("SELECT * FROM doctors WHERE status='Available'")
    av = cursor.fetchall()

    cursor.execute("SELECT  COUNT(id) AS no_of_docs FROM doctors ")
    td = cursor.fetchone()

    cursor.execute(
        "SELECT  COUNT(id) AS no_of_patient FROM online_appointment ")
    tp = cursor.fetchone()

    cursor.execute(
        "SELECT  COUNT(id ) AS no_of_docs_avl FROM doctors WHERE status='Available'")
    da = cursor.fetchone()

    cursor.execute("SELECT total_slot FROM slots")
    sl = cursor.fetchone()

    cursor.execute("SELECT date AS Date, COUNT(id ) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE() ")
    total = cursor.fetchone()

    cursor.execute("SELECT * FROM slider")
    slider = cursor.fetchall()

    # for medicine adding

    cursor.execute("SELECT * FROM product")
    med = cursor.fetchall()

    if request.method == 'POST':

        status = request.form['status']

        cursor.execute(
            "UPDATE doctors SET status = %s WHERE id= %s", (status, id))
        conn.commit()
        return redirect('admin_dashboard')
    
    return render_template("admin_dashboard.html", admin=admin, pd=pd, doc=doc, av=av, td=td, da=da, 
    tp=tp,emp=emp,sl=sl,total=total,emp_avl=emp_avl,slider=slider,med=med)

@app.route('/super_admin_dashboard')
def super_admin_dashboard():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        " SELECT date AS Date, COUNT(id) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE();")
    admin = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM online_appointment WHERE date(date) = CURDATE();")
    pd = cursor.fetchall()
    cursor.execute("SELECT * FROM doctors")
    doc = cursor.fetchall()

    cursor.execute("SELECT * FROM employee")
    emp = cursor.fetchall()

    cursor.execute("SELECT * FROM doctors WHERE status='Available'")
    av = cursor.fetchall()

    cursor.execute("SELECT  COUNT(id ) AS no_of_docs FROM doctors ")
    td = cursor.fetchone()

    cursor.execute('SELECT COUNT(id) AS no_of_emps FROM employee')
    te = cursor.fetchone()

    cursor.execute(
        "SELECT  COUNT(id) AS no_of_patient FROM online_appointment ")
    tp = cursor.fetchone()

    cursor.execute(
        "SELECT  COUNT(id ) AS no_of_docs_avl FROM doctors WHERE status='Available'")
    da = cursor.fetchone()

    cursor.execute("SELECT total_slot FROM slots")
    sl = cursor.fetchone()

    cursor.execute(
        "SELECT date AS Date, COUNT(id ) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE() ")
    total = cursor.fetchone()

    if request.method == 'POST':

        status = request.form['status']

        cursor.execute(
            "UPDATE doctors SET status = %s WHERE id= %s", (status, id))
        conn.commit()
        return redirect('super_admin_dashboard')
    return render_template('super_admin_dashboard.html', admin=admin, pd=pd, doc=doc, av=av, td=td, te=te, da=da, tp=tp, emp=emp, sl=sl, total=total)


@app.route('/slider',methods=['GET','POST'])
def slider():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
            
            content_sl1 = request.form['content_sl1']
            content_sl2 = request.form['content_sl2']
            content_sl3 = request.form['content_sl3']
            content_sl4 = request.form['content_sl4']

            cursor.execute("UPDATE slider SET content_sl1=%s,content_sl2=%s,content_sl3=%s,content_sl4=%s WHERE name='slider' ",
            (content_sl1,content_sl2,content_sl3,content_sl4))
            conn.commit()
            return redirect('admin_dashboard')

            
    if request.method == 'POST':
    
            sl1 = request.files.getlist('sl1[]')
            # print(files)
            for files in sl1 :
                if files and allowed_file(files.filename):
                    filename = secure_filename(files.filename)
                    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("UPDATE slider SET sl1=%s WHERE name='slider' ", [filename])
                    cursor.fetchall()
                    conn.commit()
                return redirect('admin_dashboard')
    if request.method == 'POST':
            sl2 = request.files.getlist('sl2[]')
            
            # print(files)
            for files in sl2 :
                if files and allowed_file(files.filename):
                    filename = secure_filename(files.filename)
                    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("UPDATE slider SET sl2=%s WHERE name='slider' ", [filename])
                    cursor.fetchall()
                    conn.commit()
                return redirect('admin_dashboard')
    if request.method == 'POST':
            
            sl3 = request.files.getlist('sl3[]')

            # print(files)
            for files in sl3 :
                if files and allowed_file(files.filename):
                    filename = secure_filename(files.filename)
                    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("UPDATE slider SET sl3=%s WHERE name='slider' ", [filename])
                    cursor.fetchall()
                    conn.commit()
                return redirect('admin_dashboard')
    if request.method == 'POST':
           
            sl4 = request.files.getlist('sl4[]')

            # print(files)
            for files in sl4 :
                if files and allowed_file(files.filename):
                    filename = secure_filename(files.filename)
                    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cursor.execute("UPDATE slider SET sl4=%s WHERE name='slider' ", [filename])
                    cursor.fetchall()
                    conn.commit()
                return redirect('admin_dashboard')
    return render_template("admin_dashboard.html")

# --------------------------Slot Update------------------------------

@app.route('/slots', methods=['GET', 'POST'])
def slots():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':

        total_slot = request.form['total_slot']

        cursor.execute(
            "UPDATE slots SET total_slot = %s", (total_slot))
        conn.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('slots.html')

# ---------------------------End Of Slot Update----------------------------



# ---------------------------Slot Booking After login----------------------


@app.route('/index', methods=['GET', 'POST'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        'SELECT file_name FROM user_login WHERE email="'+session['email']+'"')
    profile = cursor.fetchone()
    cursor.execute("SELECT date AS Date, COUNT(id ) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE() ")
    total = cursor.fetchone()
    cursor.execute("SELECT total_slot FROM slots")
    sl = cursor.fetchone()
    cursor.execute('SELECT * from slider ')
    slider = cursor.fetchall()

    msg = ''
    if request.method == 'POST':
        mobile = request.form['mobile']
        email = request.form['email']
        gender = request.form['gender']
        date = request.form['date']
        name = request.form['name']
        address = request.form['address']
        age = request.form['age']
        problem = request.form['problem']

        
        cursor.execute(
            "SELECT date AS Date, COUNT(id ) AS no_of_rows FROM online_appointment WHERE date(date)= CURDATE() ")
        total_app = cursor.fetchone()
        cursor.execute("SELECT total_slot FROM slots")
        sl = cursor.fetchone()

        if total_app['no_of_rows'] == sl['total_slot']:
            msg = 'All slots are booked'
            return render_template('index.html', msg=msg,profile=profile,total=total,sl=sl)
        else:

            cursor.execute("INSERT INTO online_appointment(mobile,email,gender,date,name,address,age,problem) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                           (mobile, email, gender, date, name, address, age, problem))

            conn.commit()
            cursor.close()
            mail.send_message('New Appointment Booking' + email,
                              sender=email,
                              recipients=[params['gmail-user']],
                              body=name + "\n" + email
                              )
            ms = Message('Heal Plus', sender='username@gmail.com',
                         recipients=[email])
            ms.body = str('Dear \n' + name + '\n'+'Your Appointment Was Booked Successfully On Date ' + date + '  in between 9Am to 3pm. \n'
                          + 'Important Notice \n'+'Please Bring Your Original Id Card At The Time Of Consultation.\n\n Thank You\nTeam Heal Plus')
            mail.send(ms)
            return redirect('index_view_appointment')
    return render_template("index.html", profile=profile, total=total,sl=sl,slider=slider)

# ---------------------------End-----------------------------------


@app.route('/index_view_appointment', methods=['GET', 'POST'])
def index_view_appointment():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        'SELECT file_name FROM user_login WHERE email="'+session['email']+'"')
    profile = cursor.fetchone()
    msg = ''
    if request.method == 'POST' and 'mobile' in request.form:
        # Create variables for easy access
        mobile = request.form['mobile']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM online_appointment WHERE mobile = %s ', (mobile, ))
        # Fetch one record and return result
        account = cursor.fetchall()
        if account:
            return render_template('index_list_appointment.html', account=account, profile=profile)
        # # If account exists in accounts table in out database
        # if account:
        #     # Create session data, we can access this data in other routes
        #     session['loggedin'] = True
        #     session['mobile'] = account['mobile']
        #     # Redirect to home page
        #     # return 'Logged in successfully!'
        #     return render_template('index_list_appointment.html', account=account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index_view_appointment.html', msg=msg, profile=profile)


@app.route('/print_appointment')
def index_print_appointment():
    conn = mysql.connect()
    # profile image
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        'SELECT file_name FROM user_login WHERE email="'+session['email']+'"')
    profile = cursor.fetchone()
    #  End profile image
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute(
            'SELECT * FROM online_appointment WHERE mobile = %s', [session['mobile']])
        jk = cursor.fetchone()
        # Show the profile page with account info
        return render_template('index_list_appointment.html', jk=jk, profile=profile)
    # return redirect(url_for('home2'))


@app.route('/appointment', methods=['GET', 'POST'])
def appointment2():
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        d_id = request.form['d_id']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        specialization = request.form['specialization']
        department = request.form['department']
        age = request.form['age']
        gender = request.form['gender']
        bloodgroup = request.form['bloodgroup']
        address = request.form['address']
        status = request.form['status']

        cursor.execute("INSERT INTO doctors(d_id,name,phone,email,specialization,department,age,gender,bloodgroup,address,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       (d_id, name, phone, email, specialization, department, age, gender, bloodgroup, address, status))

        conn.commit()
        cursor.close()
        return redirect('admin_dashboard')
    return render_template("appointment.html")


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':

        status = request.form['status']

        cursor.execute(
            "UPDATE doctors SET status = %s WHERE id= %s", (status, id))
        conn.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('update.html')


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_doctors(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM doctors WHERE id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/add_employees',methods=['GET','POST'])
def add_employees():
# connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
            e_id = request.form['e_id']
            name  = request.form['name']
            email= request.form['email']
            address = request.form['address']
            gender= request.form['gender']
            phone= request.form['phone']
            dob= request.form['dob']
            bloodgroup= request.form['bloodgroup']
            age= request.form['age']
            designation = request.form['designation']
            department = request.form['department']
            status = request.form['status']
            
            cursor.execute("INSERT INTO employee(e_id,name,email,address,gender,phone,dob,bloodgroup,age,designation,department,status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e_id,name,email,address,gender,phone,dob,bloodgroup,age,designation,department,status))
            
            if request.method == 'POST':
                photo = request.files.getlist('photo[]')
            # print(files)
                for file in photo:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        cursor.execute("UPDATE employee SET photo=%s WHERE e_id=%s", [filename,e_id])
                        cursor.fetchone()
            conn.commit()
            cursor.close()
        
            return redirect('admin_dashboard')
    return render_template("add_employees.html")        


@app.route('/delete_employee/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    msg = ''
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute('DELETE FROM employee WHERE id = {0}'.format(id))
    conn.commit()
    msg = 'Employee Removed Successfully'
    return redirect(url_for('admin_dashboard'))
                                                       

# -----------------------middle_ware_route----------------------

@app.route('/middle_ware', methods=['GET', 'POST'])
def middle_ware():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM attendance WHERE date=CURDATE()")
    att = cursor.fetchall()


    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        date = request.form['date']
        address = request.form['address']
        p_name = request.form['p_name']
        p_id = request.form['p_id']
        quantity = request.form['quantity']
        price_unit = request.form['price_unit']
        cursor.execute("INSERT INTO billing(name,mobile,email,date,address,p_name,p_id,quantity,price_unit) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                       (name, mobile, email, date, address, p_name, p_id, quantity, price_unit))
        if request.method == 'POST':
            cursor.execute(
                "UPDATE billing SET `with_gst`=((price_unit*18)/100) ")
        if request.method == 'POST':
            cursor.execute(
                "UPDATE billing SET `total_price`=((quantity*price_unit)+with_gst) ")
        conn.commit()
        cursor.close()
        return redirect('viewbills')

    return render_template("middle_ware.html",att=att)


@app.route('/viewbills', methods=['GET', 'POST'])
def viewbills():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''
    if request.method == 'POST' and 'mobile' in request.form:
        # Create variables for easy access
        # name = request.form['name']

        mobile = request.form['mobile']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM billing WHERE  mobile = %s ', (mobile, ))
        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['name'] = account['name']
            session['mobile'] = account['mobile']

            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect('list_bill')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('viewbills.html', msg=msg)


@app.route('/list_bill', methods=['GET', 'POST'])
def list_bill():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor.execute('SELECT * FROM billing WHERE mobile = %s',
                       [session['mobile']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('list_bill.html', account=account)


@app.route('/bill_invoice/<string:id>')
def bill_invoice(id):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT name,mobile,email,date,p_name,p_id,quantity,price_unit,with_gst,total_price FROM billing WHERE id=%s", (id,))
    # result=cursor.execute("SELECT  * FROM sales WHERE id=%s",(id,) )
    employee = cursor.fetchall()
    cursor.close()
    res = render_template('bill_invoice.html', employee=employee)
    responsestring = pdfkit.from_string(res, False)
    response = make_response(responsestring)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=invoice.pdf'
    return response

@app.route('/attendance',methods=['GET','POST'])
def attendance():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''
    

    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        shift = request.form['shift']
        intime = request.form['intime']
        late = request.form['late']

        cursor.execute("INSERT INTO attendance(name,date,shift,intime,late) VALUES(%s,%s,%s,%s,%s) ",(name,date,shift,intime,late))
        conn.commit()
        msg='Added Successfully.'
        return redirect('middle_ware')
    return render_template('middle_ware.html',msg=msg)

@app.route('/attendance_edit/<string:id>',methods=['GET','POST'])
def attendance_edit(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg=''

    cursor.execute("SELECT * FROM attendance WHERE id=%s",(id))
    at = cursor.fetchall()

    if request.method == 'POST':
        
        outtime = request.form['outtime']
        earlyleaving = request.form['earlyleaving']
        overtime = request.form['overtime']
        totaltime = request.form['totaltime']

        cursor.execute("UPDATE attendance SET outtime=%s,earlyleaving=%s,overtime=%s,totaltime=%s WHERE id=%s ",
        (outtime,earlyleaving,overtime,totaltime,id))
        conn.commit()
        return redirect(url_for('middle_ware'))
    return render_template('attendance_edit.html',at=at)
@app.route('/attendance_delete/<string:id>',methods=['GET','POST'])
def attendance_delete(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("DELETE FROM attendance WHERE id={0}".format(id))
    conn.commit()
    return redirect(url_for("middle_ware"))

# ----------------------------------------------- End Middle Ware------------------------------------------------



@app.route('/about')
def about():
    conne = mysql.connect()
    cur = conne.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT file_name FROM user_login WHERE email="' +
                session['email'] + '"')
    profile = cur.fetchone()

    cur.execute("SELECT * FROM employee")
    ab = cur.fetchall()

    return render_template("about.html", profile=profile,ab=ab)
# -----------------------------for doctor booking-----------------------------
@app.route('/book_doctor/<string:id>',methods=['GET','POST'])
def book_doctor(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    msg = ''

    cursor.execute("SELECT * FROM employee")
    ab = cursor.fetchall()

    cursor.execute('SELECT file_name FROM user_login WHERE email="' +
                session['email'] + '"')
    profile = cursor.fetchone()

    cursor.execute("SELECT * FROM employee WHERE id=%s",(id))
    dc = cursor.fetchall()

    if request.method == 'POST':
        date = request.form['date']
        doctor_name = request.form['doctor_name']
        doctor_department = request.form['doctor_department']
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        patient_bloodgroup = request.form['patient_bloodgroup']
        patient_gender = request.form['patient_gender']
        patient_mobile = request.form['patient_mobile']
        patient_email = request.form['patient_email']

        patient_address = request.form['patient_address']

        cursor.execute("""INSERT INTO ap_doctor(date,doctor_name,doctor_department,patient_name,patient_age,patient_bloodgroup,patient_gender,patient_mobile,patient_email,patient_address)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,(date,doctor_name,doctor_department,patient_name,patient_age,patient_bloodgroup,patient_gender,patient_mobile,patient_email,patient_address))
        conn.commit()
        cursor.close()
        msg = 'Appointment Booked Successfully.Please Check Your Email for Details'

        mail.send_message('New Appointment Booking' + patient_email,
                              sender=patient_email,
                              recipients=[params['gmail-user']],
                              body=patient_name + "\n" + patient_email
                              )
        ms = Message('Heal Plus', sender='username@gmail.com',
                         recipients=[patient_email])
        ms.body = str('Dear \n' +patient_name + '\n'+'Your Appointment Was Booked Successfully On Date ' + date + '  in between 9Am to 3pm. \n'
                          'Doctors Name - ' +doctor_name+ '\n' 'Department - '+doctor_department+ '\n' + 'Important Notice \n'+'Please Bring Your Original Id Card At The Time Of Consultation.\n\n Thank You\nTeam Heal Plus')
        mail.send(ms)
        return redirect(url_for('about'))
    return render_template("book_doctor.html",dc=dc,msg=msg,profile=profile,ab=ab)







@app.route('/services')
def services():
    conne = mysql.connect()
    cur = conne.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT file_name FROM user_login WHERE email="' +
                session['email'] + '"')
    profile = cur.fetchone()
    return render_template("services.html", profile=profile)


@app.route('/contact')
def contact():
    conne = mysql.connect()
    cur = conne.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT file_name FROM user_login WHERE email="' +
                session['email'] + '"')
    profile = cur.fetchone()
    return render_template("contact.html", profile=profile)


@app.route('/pl_about')
def pl_about():
    return render_template("pl_about.html")


@app.route('/pl_services')
def pl_services():
    return render_template("pl_services.html")


@app.route('/pl_contact')
def pl_contact():
    return render_template("pl_contact.html")


@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    conne = mysql.connect()
    cursor = conne.cursor(pymysql.cursors.DictCursor)
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM user_login WHERE email=%s',
                       [session['email']])
        profile = cursor.fetchone()
        return render_template('user_profile.html', profile=profile)


@app.route('/edit_user_profile', methods=['GET', 'POST'])
def edit_user_profile():
    conne = mysql.connect()
    cursor = conne.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_login WHERE email=%s',
                   [session['email']])
    profile = cursor.fetchone()
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        gender = request.form.get('gender')
        state = request.form.get('state')
        address = request.form.get('address')
        cursor.execute(
            "UPDATE user_login SET  mobile=%s, gender=%s, state=%s, address=%s WHERE email='" + session['email'] + "'", (mobile, gender, state, address))
        conne.commit()
        return redirect('user_profile')
    return render_template('edit_user_profile.html', profile=profile)


@app.route("/upload_profile", methods=["POST", "GET"])
def upload_profile():
    conne = mysql.connect()
    cur = conne.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        # print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("UPDATE user_login SET  file_name=%s WHERE email='" +
                            session['email'] + "'", [filename])
                cur.fetchone()
                conne.commit()
        cur.close()
        flash('File(s) successfully uploaded')
        return redirect('user_profile')
    return render_template('upload_profile.html')


@app.route("/healthnavbar2", methods=["POST", "GET"])
def healthnavbar2():
    conne = mysql.connect()
    cur = conne.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT file_name FROM user_login WHERE email="' +
                session['email'] + '" ')
    profile = cur.fetchone()
    return render_template('healthnavbar2.html', profile=profile)

# --------------------Pharmacy-----------------------------------------------------------------------------------------


@app.route('/medicine', methods=['GET','POST'])
def medicine():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        code = request.form['code']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        search_metadata = request.form['search_metadata']
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

                cursor.execute('INSERT INTO product(code, name, price, quantity, search_metadata, file ) '
                               'VALUES (%s,%s,%s,%s,%s,%s)',
                               (code, name, price, quantity, search_metadata, filename))
                conn.commit()
                cursor.close()
                return redirect('medicine')
    return render_template('medicine.html')

@app.route('/view_cart')
def displaycart():
    return render_template('cart.html')



@app.route('/addlocation', methods=['GET','POST'])
def addlocation():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
       houseno = request.form['houseno']
       landmark = request.form['landmark']
       pincode = request.form['pincode']
       city = request.form['city']
       state = request.form['state']
       customername = request.form['customername']
       phnno = request.form['phnno']
       place = request.form['place']

       cursor.execute('INSERT INTO addlocation(houseno ,landmark ,pincode ,city ,state ,customername ,phnno, place) '
                      'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                      (houseno ,landmark ,pincode ,city ,state ,customername ,phnno , place))
       conn.commit()
    return render_template("addlocation.html")












@app.route('/add', methods=['GET','POST'])
def add_product_to_cart():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        if _quantity and _code and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM product WHERE code=%s", _code)
            row = cursor.fetchone()
            if float(row['quantity']) >= float(_quantity):
                itemArray = {row['code']: {'name': row['name'], 'code': row['code'], 'quantity': _quantity,
                                           'price': row['price'], 'image': row['file'],
                                           'total_price': _quantity * row['price']}}
                all_total_price = 0
                all_total_quantity = 0
                session.modified = True
                if 'cart_item' in session:
                    if row['code'] in session['cart_item']:
                        for key, value in session['cart_item'].items():
                            if row['code'] == key:
                                old_quantity = session['cart_item'][key]['quantity']
                                total_quantity = old_quantity + _quantity
                                session['cart_item'][key]['quantity'] = total_quantity
                                session['cart_item'][key]['total_price'] = total_quantity * row['price']
                    else:
                        session['cart_item'] = array_merge(session['cart_item'], itemArray)
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                else:
                    session['cart_item'] = itemArray
                    all_total_quantity = all_total_quantity + _quantity
                    all_total_price = all_total_price + _quantity * row['price']
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price
                return redirect(url_for('.products'))
            else:
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()
                return render_template('addtocart.html', products=rows, status='stock_error')
    except Exception as e:
        print(e)
    # finally:
    #     cursor.commit()
    #     conn.close()
    # return render_template('addtocart.html')   


@app.route('/addtocart')
def products():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM product")
        rows = cursor.fetchall()
        return render_template('addtocart.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/empty')
def empty_cart():
    try:
        session.pop('all_total_quantity')
        session.pop('all_total_price')
        session.pop('cart_item')
        return redirect(url_for('.displaycart'))
    except Exception as e:
        print(e)


@app.route('/delete_item/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True
        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break
        if all_total_quantity == 0:
            session.pop('all_total_quantity')
            session.pop('all_total_price')
            session.pop('cart_item')
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
        return redirect(url_for('.displaycart'))
    except Exception as e:
        print(e)


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


@app.route('/search', methods=['POST'])
def search():
    _search = (request.form['search'])
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM product WHERE name LIKE %s OR search_metadata LIKE %s",
                       ("%" + _search + "%", "%" + _search + "%",))
        rows = cursor.fetchall()
        if not rows:
            return redirect(url_for('.products'))
        else:
            return render_template('addtocart.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
