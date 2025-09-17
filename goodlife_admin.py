from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = 'goodlife_schema.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Visitor Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            aadhar TEXT,
            age INTEGER,
            address TEXT,
            purpose TEXT,
            remarks TEXT,
            visit_date DATE
        )
    ''')
    
    # Donation Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT,
            amount REAL,
            items_donated TEXT,
            payment_mode TEXT,
            payment_detail TEXT,
            donation_date DATE
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/visitor', methods=['GET', 'POST'])
def visitor():
    if request.method == 'POST':
        name = request.form['name']
        aadhar = request.form['aadhar']
        age = request.form['age']
        address = request.form['address']
        purpose = request.form['purpose']
        remarks = request.form['remarks']
        visit_date = date.today()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO visitors (name, aadhar, age, address, purpose, remarks, visit_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, aadhar, age, address, purpose, remarks, visit_date))
        conn.commit()
        conn.close()
        return render_template('success.html', message="Visitor entry submitted successfully!")
    
    return render_template('visitor_form.html')

@app.route('/donation', methods=['GET', 'POST'])
def donation():
    if request.method == 'POST':
        donor_name = request.form['donor_name']
        amount = request.form['amount']
        items_donated = request.form['items_donated']
        payment_mode = request.form['payment_mode']
        payment_detail = request.form.get('payment_detail', '')
        donation_date = date.today()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO donations (donor_name, amount, items_donated, payment_mode, payment_detail, donation_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (donor_name, amount, items_donated, payment_mode, payment_detail, donation_date))
        conn.commit()
        conn.close()
        return render_template('success.html', message="Donation entry submitted successfully!")
    
    return render_template('donation_form.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

