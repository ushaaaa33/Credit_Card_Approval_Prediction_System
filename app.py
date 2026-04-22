from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import joblib
import numpy as np
from datetime import datetime
import os

# Import email notification system

try:
    from email_utils import EmailNotifier, notify_status_change
    EMAIL_ENABLED = True
    print("✅ Email notifications ENABLED")
except ImportError as e:
    EMAIL_ENABLED = False
    print("⚠️  Email notifications DISABLED")
    print(f"   Reason: {e}")
    print("   Place email_utils.py in the same directory to enable emails")

app = Flask(__name__)
app.secret_key = 'smartcredit_secret_key_2024_change_this'

# Encodings for categorical variables
GENDER_ENC = {"F": 0, "M": 1}
OWN_CAR_ENC = {"N": 0, "Y": 1}
OWN_REALTY_ENC = {"N": 0, "Y": 1}
INCOME_TYPE_ENC = {
    "Commercial associate": 0, 
    "Pensioner": 1, 
    "State servant": 2, 
    "Student": 3, 
    "Working": 4
}
EDUCATION_TYPE_ENC = {
    "Academic degree": 0, 
    "Higher education": 1, 
    "Incomplete higher": 2, 
    "Lower secondary": 3, 
    "Secondary / secondary special": 4
}
FAMILY_STATUS_ENC = {
    "Civil marriage": 0, 
    "Married": 1, 
    "Separated": 2, 
    "Single / not married": 3, 
    "Widow": 4
}
HOUSING_TYPE_ENC = {
    "Co-op apartment": 0, 
    "House / apartment": 1, 
    "Municipal apartment": 2, 
    "Office apartment": 3, 
    "Rented apartment": 4, 
    "With parents": 5
}
WORK_PHONE_ENC = {"No": 0, "Yes": 1}
OCCUPATION_TYPE_ENC = {
    "Accountants": 0, "Cleaning staff": 1, "Cooking staff": 2, 
    "Core staff": 3, "Drivers": 4, "HR staff": 5, 
    "High skill tech staff": 6, "IT staff": 7, "Laborers": 8, 
    "Low-skill Laborers": 9, "Managers": 10, "Medicine staff": 11, 
    "Occupation Not Identified": 12, "Private service staff": 13, 
    "Realty agents": 14, "Sales staff": 15, "Secretaries": 16, 
    "Security staff": 17, "Waiters/barmen staff": 18
}

def get_db_connection():
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):    #  Hash password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    
    # Applications table
    c.execute('''CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    gender TEXT,
                    own_car TEXT,
                    own_realty TEXT,
                    children INTEGER,
                    total_income REAL,
                    income_type TEXT,
                    education_type TEXT,
                    family_status TEXT,
                    housing_type TEXT,
                    age INTEGER,
                    experience REAL,
                    work_phone TEXT,
                    occupation_type TEXT,
                    fam_members INTEGER,
                    prediction TEXT,
                    status TEXT DEFAULT 'pending',
                    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )''')
    
    # Create default admin if not exists
    c.execute("SELECT * FROM users WHERE email='admin@smartcredit.com'")
    if not c.fetchone():
        admin_password = hash_password('admin123')
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                  ('Admin', 'admin@smartcredit.com', admin_password, 'admin'))
    
    conn.commit()
    conn.close()

def load_model():
    """Load the trained ML model"""
    try:
        model = joblib.load("custom_decision_tree.pkl")
        return model
    except:
        print("⚠️ Model file not found. Please run train.py first!")
        return None

# Load model at startup
ml_model = load_model()

def predict_approval(form_data):
    """Predict credit card approval using ML model"""
    if ml_model is None:
        return "Rejected"  # Default if model not loaded
    
    try:
        # Prepare input features
        features = [
            GENDER_ENC[form_data['gender']],
            OWN_CAR_ENC[form_data['own_car']],
            OWN_REALTY_ENC[form_data['own_realty']],
            int(form_data['children']),
            float(form_data['total_income']),
            INCOME_TYPE_ENC[form_data['income_type']],
            EDUCATION_TYPE_ENC[form_data['education_type']],
            FAMILY_STATUS_ENC[form_data['family_status']],
            HOUSING_TYPE_ENC[form_data['housing_type']],
            int(form_data['age']),
            float(form_data['experience']),
            WORK_PHONE_ENC[form_data['work_phone']],
            OCCUPATION_TYPE_ENC[form_data['occupation_type']],
            int(form_data['fam_members'])
        ]
        
        # Reshape for prediction
        input_data = np.array([features])
        prediction = ml_model.predict(input_data)[0]
        
        return "Approved" if prediction == 1 else "Rejected"
    except Exception as e:
        print(f"Prediction error: {e}")
        return "Rejected"


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                           (email, password)).fetchone()
        conn.close()
        
        if user:
            # Check if user is trying to login as admin from user login page
            if user['role'] == 'admin':
                flash('⚠️ Admins must use the Admin Login page!', 'error')
                return redirect(url_for('admin_login'))
            
            # Regular user login
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Invalid email or password!', 'error')
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard - Shows user's applications"""
    # Check if user is logged in
    if 'user_id' not in session or session.get('user_role') != 'user':
        flash('⚠️ Please login to access dashboard', 'error')
        return redirect(url_for('login'))
    
    # Get user details from database
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id=?", 
                       (session['user_id'],)).fetchone()
    
    # Get user's applications
    applications = conn.execute("""
        SELECT * FROM applications 
        WHERE user_id=? 
        ORDER BY applied_date DESC
    """, (session['user_id'],)).fetchall()
    
    conn.close()
    
    # Render dashboard template
    return render_template('dashboard.html', user=user, applications=applications)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login - Administrators only"""
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                           (email, password)).fetchone()
        conn.close()
        
        if user:
            # Check if user is actually an admin
            if user['role'] != 'admin':
                flash('⚠️ Access Denied! This is for administrators only.', 'error')
                flash('Please use the regular user login page.', 'error')
                return redirect(url_for('login'))
            
            # Admin login successful
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            
            flash(f'🔐 Admin access granted. Welcome, {user["name"]}!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('❌ Invalid admin credentials!', 'error')
            # Log failed admin login attempt (optional but recommended)
            print(f"⚠️ Failed admin login attempt for: {email}")
    
    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    """Logout user or admin"""
    # Check if admin or user
    is_admin = session.get('user_role') == 'admin'
    user_name = session.get('user_name', 'User')
    
    # Clear session
    session.clear()
    
    # Show appropriate message and redirect
    if is_admin:
        flash(f'Admin {user_name} logged out successfully!', 'success')
        return redirect(url_for('admin_login'))
    else:
        flash(f'{user_name} logged out successfully!', 'success')
        return redirect(url_for('login'))
    

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    """Credit card application - NOW WITH EMAIL NOTIFICATIONS!"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        form_data = {
            'gender': request.form['gender'],
            'own_car': request.form['own_car'],
            'own_realty': request.form['own_realty'],
            'children': request.form['children'],
            'total_income': request.form['total_income'],
            'income_type': request.form['income_type'],
            'education_type': request.form['education_type'],
            'family_status': request.form['family_status'],
            'housing_type': request.form['housing_type'],
            'age': request.form['age'],
            'experience': request.form['experience'],
            'work_phone': request.form['work_phone'],
            'occupation_type': request.form['occupation_type'],
            'fam_members': request.form['fam_members']
        }
        
        # Get ML prediction
        prediction = predict_approval(form_data)
        
        # Save to database
        conn = get_db_connection()
        cursor = conn.execute("""INSERT INTO applications 
                       (user_id, gender, own_car, own_realty, children, 
                        total_income, income_type, education_type, family_status, 
                        housing_type, age, experience, work_phone, 
                        occupation_type, fam_members, prediction)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (session['user_id'], form_data['gender'], form_data['own_car'],
                     form_data['own_realty'], form_data['children'], form_data['total_income'],
                     form_data['income_type'], form_data['education_type'], form_data['family_status'],
                     form_data['housing_type'], form_data['age'], form_data['experience'],
                     form_data['work_phone'], form_data['occupation_type'], form_data['fam_members'],
                     prediction))
        
        # ===== EMAIL NOTIFICATION: APPLICATION RECEIVED =====
        application_id = cursor.lastrowid  # Get the ID of just-created application
        
        # Get user details for sending email
        user = conn.execute("SELECT * FROM users WHERE id=?", (session['user_id'],)).fetchone()
        conn.commit()
        conn.close()
        
        # Send email notification (only if email system is enabled)
        if EMAIL_ENABLED:
            try:
                print(f"\n📧 Sending 'Application Received' email to {user['email']}...")
                notifier = EmailNotifier()
                email_sent = notifier.send_application_received(
                    user_name=user['name'],
                    user_email=user['email'],
                    application_id=application_id,
                    ml_prediction=prediction
                )
                
                if email_sent:
                    flash(f'Application submitted! ML Prediction: {prediction}. ✉️ Check your email for confirmation.', 'success')
                else:
                    flash(f'Application submitted! ML Prediction: {prediction}. (Email notification failed)', 'success')
            except Exception as e:
                print(f"❌ Email error: {e}")
                flash(f'Application submitted! ML Prediction: {prediction}', 'success')
        else:
            flash(f'Application submitted! ML Model Prediction: {prediction}', 'success')
        
        return redirect(url_for('dashboard'))
    
    return render_template('apply.html')


@app.route('/admin')
def admin():
    """Admin dashboard - Require admin role"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('⚠️ Please login to access admin dashboard', 'error')
        return redirect(url_for('admin_login'))  # Changed from 'login'
    
    # Check if user is actually an admin
    if session.get('user_role') != 'admin':
        flash('⚠️ Access Denied! Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    applications = conn.execute("""
        SELECT a.*, u.name, u.email 
        FROM applications a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.applied_date DESC
    """).fetchall()
    
    users = conn.execute("SELECT * FROM users WHERE role='user'").fetchall()
    
    # Statistics
    total = len(applications)
    approved = len([a for a in applications if a['status'] == 'approved'])
    rejected = len([a for a in applications if a['status'] == 'rejected'])
    pending = len([a for a in applications if a['status'] == 'pending'])
    
    conn.close()
    
    return render_template('admin.html', 
                          applications=applications,
                          users=users,
                          stats={'total': total, 'approved': approved, 
                                'rejected': rejected, 'pending': pending})


@app.route('/admin/update/<int:app_id>/<status>')
def update_status(app_id, status):
    """Update application status - NOW SENDS EMAIL TO USER!"""
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    
    # Get application and user details BEFORE updating
    conn = get_db_connection()
    app_data = conn.execute("""
        SELECT a.*, u.name, u.email 
        FROM applications a
        JOIN users u ON a.user_id = u.id
        WHERE a.id = ?
    """, (app_id,)).fetchone()
    
    if not app_data:
        flash('Application not found!', 'error')
        conn.close()
        return redirect(url_for('admin'))
    
    # Update application status in database
    conn.execute("UPDATE applications SET status=? WHERE id=?", (status, app_id))
    conn.commit()
    conn.close()
    
    # ===== EMAIL NOTIFICATION: APPROVED/REJECTED =====
    if EMAIL_ENABLED:
        try:
            print(f"\n📧 Sending '{status}' notification email to {app_data['email']}...")
            
            # Send appropriate email based on status
            email_sent = notify_status_change(
                user_name=app_data['name'],
                user_email=app_data['email'],
                application_id=app_id,
                status=status,
                income=app_data['total_income']  # Needed for credit limit calculation
            )
            
            if email_sent:
                flash(f'✅ Application {status}! ✉️ Email notification sent to {app_data["email"]}', 'success')
            else:
                flash(f'Application {status}! (Email notification failed)', 'warning')
                
        except Exception as e:
            print(f"❌ Email notification error: {e}")
            flash(f'Application {status}! (Email notification failed: {str(e)})', 'warning')
    else:
        flash(f'Application {status} successfully!', 'success')
    # =================================================
    
    return redirect(url_for('admin'))

# APP STARTUP

if __name__ == '__main__':
    init_db()
    print("\n" + "=" * 70)
    print("🏦 SmartCredit Banking System - Starting Server")
    print("=" * 70)
    print("\n🔌 Default Admin Credentials:")
    print("   Email: admin@smartcredit.com")
    print("   Password: admin123")
    print("\n🌐 Server: http://127.0.0.1:5000")
    
    if EMAIL_ENABLED:
        print("\n📧 Email Notifications: ✅ ENABLED")
        print("   ✉️  Application Received - Sent when user submits form")
        print("   ✉️  Approved - Sent when admin approves")
        print("   ✉️  Rejected - Sent when admin rejects")
        print("\n⚙️  Configure email in: email_utils.py (lines 25-26)")
    else:
        print("\n📧 Email Notifications: ⚠️  DISABLED")
        print("   To enable: Place email_utils.py in the same directory")
    
    print("=" * 70 + "\n")
    
    app.run(debug=True, port=5000)