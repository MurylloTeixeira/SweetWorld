import sqlite3
from werkzeug.security import generate_password_hash

usuario = "admin"
senha = "1234"

senha_hash = generate_password_hash(senha)

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
    (usuario, senha_hash)
)

conn.commit()
conn.close()

print("Usuario criado!")