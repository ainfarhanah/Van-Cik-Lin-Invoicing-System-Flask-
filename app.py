from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import base64

app = Flask(__name__)
app.secret_key = "Van Cik Lin v1.0"

mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vanciklinv1'

#Inject logo as base64 for all templates
@app.context_processor
def inject_logo():
    with open("static/images/logo.png", "rb") as img:
        logo = base64.b64encode(img.read()).decode("utf-8")
    return dict(logo_base64=logo)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    title = "Register"

    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Please fill out the form.','danger')
            return redirect(url_for('register'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s",(username,))
        user = cursor.fetchone()

        if user:
            flash('Account is already exist.', 'danger')
            return redirect(url_for('register'))
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT into users (username,email,password) VALUES (%s,%s,%s)",(username,email,hashed_password))
            mysql.connection.commit()
            flash('You have successfully registered', 'success')

            return redirect(url_for('register'))
        
    return render_template('register.html', title=title)



if __name__ == '__main__':
    app.run(debug=True)