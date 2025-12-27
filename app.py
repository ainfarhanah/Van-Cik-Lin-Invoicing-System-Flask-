from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os
from pathlib import Path

app = Flask(__name__)
# Load secret key from environment with a safe fallback for local development
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret')

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vanciklinv1'

# Cache logo at startup to avoid opening the file on every request
_logo_path = Path('static') / 'images' / 'logo.png'
try:
    with _logo_path.open('rb') as _img:
        APP_LOGO_BASE64 = base64.b64encode(_img.read()).decode('utf-8')
except Exception:
    APP_LOGO_BASE64 = ''

mysql = MySQL(app)

#Inject logo as base64 for all templates
@app.context_processor
def inject_logo():
    return dict(logo_base64=APP_LOGO_BASE64)

@app.route('/')
def home():
    title = "Login"
    if 'loggedin' not in session:
        return render_template('login.html', title=title)
    else:
        return redirect(url_for('dashboard'))

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
            cursor.execute("INSERT into users (username,email,password) VALUES (%s,%s,%s)", (username,email,hashed_password))
            mysql.connection.commit()
            flash('You have successfully registered', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    if 'loggedin' not in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE username = %s",(username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['loggedin'] = True
                session['id'] = user['userID']
                session['username'] = user['username']
                flash('You have successfully logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect username/password!', 'danger')
                return redirect(url_for('login'))
        return render_template('login.html', title=title)
    else:
        return redirect(url_for('dashboard'))
    
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        title = "Dashboard"
        return render_template('dashboard.html', username=session['username'], title=title)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        title = "Profile"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE userID = %s", (session['id'],))
        user = cursor.fetchone()
        demo = user['username']=='demo'
        return render_template('profile.html', user=user, title=title, demo=demo)
    else:
        return redirect(url_for('login'))

@app.route('/updateprofile', methods=['POST'])
def updateprofile():
    if 'loggedin' in session:
        username = request.form['username']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        new_password = request.form.get('password', '').strip()
        if new_password:
            hashed = generate_password_hash(new_password)
            cursor.execute(
            'UPDATE users SET username=%s, email=%s, password=%s WHERE userID=%s',
            (username, email, hashed, session['id'])
            )
        else:
            cursor.execute(
            'UPDATE users SET username=%s, email=%s WHERE userID=%s',
            (username, email, session['id'])
            )
        mysql.connection.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)