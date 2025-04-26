from flask import Flask, render_template, request, redirect, url_for , session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='',  
        database='student_management'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Database connection
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM appuser WHERE username = %s AND role = 'student'", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        # If the user does not exist, return error
        if not user:
            return "Invalid username or password"

        # Check if the entered password matches the stored hash
        if check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM appuser WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            connection.close()
            return "Username already exists"

        # Insert new user with hashed password and 'student' role
        cursor.execute("INSERT INTO appuser (username, password, role) VALUES (%s, %s, %s)", 
                       (username, hashed_password, 'student'))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('view_students'))
    return render_template('add_student.html')

@app.route('/view_students')
def view_students():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_students.html', students=students)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        course_code = request.form['course_code']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO courses (course_name, course_code) VALUES (%s, %s)", (course_name, course_code))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('add_course.html')

@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('enroll_student.html')

@app.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        date = request.form['date']
        status = request.form['status']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO attendance (student_id, course_id, date, status) VALUES (%s, %s, %s, %s)", (student_id, course_id, date, status))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('mark_attendance.html')

@app.route('/record_performance', methods=['GET', 'POST'])
def record_performance():
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        grade = request.form['grade']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO academic_performance (student_id, course_id, grade) VALUES (%s, %s, %s)", (student_id, course_id, grade))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template('record_performance.html')

if __name__ == '__main__':
    app.run(debug=True)