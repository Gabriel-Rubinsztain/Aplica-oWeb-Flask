from distutils.log import info
import os
from flask import Flask, jsonify, request, render_template, abort
import sqlite3

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return render_template('signup.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    if name and email and address:
        con = sqlite3.connect('user.db')
        cur = con.cursor()
        cur.execute(
            """INSERT INTO users (name, email, address)VALUES (?,?,?)""", (name, email, address))
        con.commit()
        cur.close()
        con.close()
        return render_template('signup.html')


@app.route('/list')
def list():
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)
    con.close()


def create_db():

    con = sqlite3.connect('user.db')

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute(
        '''CREATE TABLE users (name varchar, email varchar, address varchar)''')

    con.commit()
    con.close()


create_db()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(host='0.0.0.0', port=port)
