from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from face_recognition import recognize_faces

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Admin credentials
admin_credentials = {'admin@example.com': 'adminpassword'}

# Route: Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Route: Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in admin_credentials and admin_credentials[email] == password:
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid Admin Credentials')
    return render_template('admin_login.html')

# Route: Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    users = []
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        users = [row for row in reader]
    return render_template('admin_dashboard.html', users=users)

# Route: Student Login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with open('users.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email and row['password'] == password:
                    return "Welcome, Student!"
            flash('Invalid Student Credentials')
    return render_template('student_login.html')

# Route: Take Attendance
@app.route('/attendance')
def attendance():
    result = recognize_faces()
    return render_template('attendance.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
