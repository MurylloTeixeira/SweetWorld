from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
app = Flask(__name__)
app.secret_key = "uma-chave-super-secreta"

def get_db():
    return sqlite3.connect("database.db")
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT senha FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], senha):
            session["usuario"] = usuario
            return redirect(url_for("home"))
        else:
            return render_template("login.html", erro="Usuario ou senha invalidos")

    return render_template("login.html")

@app.route('/perfil')
def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("perfil.html", usuario=session["usuario"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        senha_hash = generate_password_hash(senha)

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                (usuario, senha_hash)
            )
            conn.commit()
            conn.close()

            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                erro="Usuario ja existe"
            )
    return render_template("register.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/explore')
def explore():
    return render_template("explore.html")

@app.route('/logout')
def logout():
    session.pop("usuario", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
