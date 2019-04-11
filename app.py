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
@app.route('/books')
def index():
    return render_template('index.html')

@app.route('/safaribabes')
def safaribabes():
    safaribabes = execute_sql('SELECT * FROM safaribabes')
    return render_template('safaribabes.html', safaribabes=safaribabes)

# @app.route('/Manga')
# def mangas():
#     mangas = execute_sql('SELECT * FROM mangas')
#     return render_template('manga.html', mangas=mangas)
#

#
# @app.route('/SciFi')
# def sciences():
#     sciences = execute_sql('SELECT * FROM sciences')
#     return render_template('SciFi.html', sciences=sciences)

if __name__ == '__main__':
    app.run(debug=True)
