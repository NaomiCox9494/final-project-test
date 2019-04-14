import sqlite3
import datetime
from flask import Flask, render_template, g, request, redirect, url_for

PATH = 'db/animalBaby.sqlite'

app = Flask(__name__)

def open_connection():
    connection = getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

        cursor.close()
        return results

@app.teardown_appcontext
def close_connection(exeption):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/safaribabes')
def safaribabes():
    safaribabes = execute_sql('SELECT * FROM safaribabes')
    return render_template('safaribabes.html', safaribabes=safaribabes)

@app.route('/tests')
def tests():
    tests = execute_sql('SELECT * FROM tests')
    return render_template('tests.html', tests=tests)

@app.route('/lamb')
def lamb():
    return render_template('lamb.html')

@app.route('/firstPage')
def firstPage():
    return render_template('firstPage.html')


if __name__ == '__main__':
    app.run(debug=True)
