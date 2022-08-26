
from flask import Flask, render_template, request, redirect
import pymysql

site_flask = Flask(__name__)

def connection():
    s = 'localhost' #Your server(host) name
    d = 'game'
    u = 'root' #Your login user
    p = '1234' #Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

@site_flask.route("/")
def main():
    players = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Player")
    for row in cursor.fetchall():
        players.append({"id": row[0], "name": row[1], "roupa": row[2], "posicao": row[3]})
    conn.close()
    return render_template("playerslist.html", players = players)
@site_flask.route("/addplayer", methods = ['GET', 'POST'])
def addplayer():
    if request.method == 'GET':
        return render_template("addplayer.html", player = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        roupa = request.form["roupa"]
        posicao = int(request.form["posicao"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Player (id, name, roupa, posicao) VALUES (%s, %s, %s, %s)", (id, name, roupa, posicao))
        conn.commit()
        conn.close()
        return redirect('/')
@site_flask.route('/updateplayer/<int:id>', methods = ['GET', 'POST'])
def updateplayer(id):
    pl = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Player WHERE id = %s", (id))
        for row in cursor.fetchall():
            pl.append({"id": row[0], "name": row[1], "roupa": row[2], "posicao": row[3]})
        conn.close()
        return render_template("addplayer.html", player = pl[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        roupa = str(request.form["roupa"])
        posicao = int(request.form["posicao"])
        cursor.execute("UPDATE Player SET name = %s, roupa = %s, posicao = %s WHERE id = %s", (name, roupa, posicao, id))
        conn.commit()
        conn.close()
        return redirect('/')
@site_flask.route('/deleteplayer/<int:id>')
def deleteplayer(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Player WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')

if(__name__ == "__main__"):
    site_flask.run()