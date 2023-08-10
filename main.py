from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database initialization and connection
conn = sqlite3.connect("motorcycle_log.db")
cursor = conn.cursor()

# Routes
@app.route('/')
def index():
    return render_template('frontend/index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    return redirect('/')

@app.route('/add_motorcycle', methods=['POST'])
def add_motorcycle():
    user_id = int(request.form['user_id'])
    brand = request.form['brand']
    model = request.form['model']
    cursor.execute("INSERT INTO motorcycles (user_id, brand, model) VALUES (?, ?, ?)", (user_id, brand, model))
    conn.commit()
    return redirect('/')

@app.route('/add_repair', methods=['POST'])
def add_repair():
    motorcycle_id = int(request.form['motorcycle_id'])
    date = request.form['date']
    particulars = request.form['particulars']
    cost = float(request.form['cost'])
    cursor.execute("INSERT INTO repairs (motorcycle_id, date, particulars, cost) VALUES (?, ?, ?, ?)", (motorcycle_id, date, particulars, cost))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
