from flask import Flask, render_template, request, redirect
import sqlite3
from queue import Queue
import threading

app = Flask(__name__)

# SQLite Connection Pool
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

# Helper Functions
def execute_query(query, *args):
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    cursor.execute(query, args)
    connection.commit()
    connection_pool.release_connection(connection)
    return cursor

# Routes
@app.route('/')
def index():
    return render_template('frontend/index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    query = "INSERT INTO users (username) VALUES (?)"
    execute_query(query, username)
    return redirect('/')

@app.route('/add_motorcycle', methods=['POST'])
def add_motorcycle():
    user_id = int(request.form['user_id'])
    brand = request.form['brand']
    model = request.form['model']
    query = "INSERT INTO motorcycles (user_id, brand, model) VALUES (?, ?, ?)"
    execute_query(query, user_id, brand, model)
    return redirect('/')

@app.route('/add_repair', methods=['POST'])
def add_repair():
    motorcycle_id = int(request.form['motorcycle_id'])
    date = request.form['date']
    particulars = request.form['particulars']
    cost = float(request.form['cost'])
    query = "INSERT INTO repairs (motorcycle_id, date, particulars, cost) VALUES (?, ?, ?, ?)"
    execute_query(query, motorcycle_id, date, particulars, cost)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
