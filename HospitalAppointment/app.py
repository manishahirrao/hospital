from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Use Vercel's tmp directory for database in production
if os.environ.get('VERCEL'):
    db_path = '/tmp/hospital.db'
else:
    db_path = 'hospital.db'

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            age INTEGER,
            doctor TEXT,
            appointment_date TEXT,
            appointment_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

@app.route('/appointments')
def appointments():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointment ORDER BY appointment_date, appointment_time")
    appointments = cursor.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

@app.route('/delete/<int:id>')
def delete_appointment(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointment WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('appointments'))

@app.route('/save', methods=['POST'])
def save():
    name = request.form['name']
    age = request.form['age']
    doctor = request.form['doctor']
    date = request.form['date']
    time = request.form['time']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = "INSERT INTO appointment (patient_name, age, doctor, appointment_date, appointment_time) VALUES (?, ?, ?, ?, ?)"
    values = (name, age, doctor, date, time)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    return render_template('success.html', date=date, time=time)

# Vercel serverless function handler
app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run(debug=True)
    print("Database connected successfully")