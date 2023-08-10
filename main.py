from flask import Flask, render_template, request, redirect
import sqlite3
import threading
from queue import Queue


app = Flask(__name__)

class SQLiteConnectionPool:
    def __init__(self, max_connections=5):
        self.max_connections = max_connections
        self.connections = Queue(maxsize=max_connections)
        for _ in range(max_connections):
            self.connections.put(self._create_connection())

    def _create_connection(self):
        return sqlite3.connect("motorcycle_log.db")

    def get_connection(self):
        return self.connections.get()

    def release_connection(self, connection):
        self.connections.put(connection)

connection_pool = SQLiteConnectionPool()

def get_cursor():
    connection = connection_pool.get_connection()
    return connection.cursor()

def release_cursor(cursor):
    connection = cursor.connection
    cursor.close()
    connection_pool.release_connection(connection)


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
