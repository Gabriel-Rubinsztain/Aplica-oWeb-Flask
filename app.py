import os
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL

app = Flask(__name__)


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mudar123'
app.config['MYSQL_DB'] = 'cadastro'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'

mysql = MySQL(app)


@app.route("/", methods=['GET'])
def home():
    return render_template('signup.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    nome = request.form['nome']
    categoria = request.form['categoria']
    preco = request.form['preco']

    if nome and categoria and preco:

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO cadastro VALUES (% s, % s, % s)', (nome, categoria, preco))
        mysql.connection.commit()
        cursor.close()
        return render_template('signup.html')


@app.route('/list')
def list():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from cadastro")
    rows = cursor.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(host='0.0.0.0', port=port)

