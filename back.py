from flask import Flask, render_template, request
import pyodbc


app = Flask("__name__")

conn = pyodbc.connect(
    "driver={ODBC Driver 18 for SQL Server};server=DESKTOP-HILI2I3;database=tcc;trusted_connection=yes;trustservercertificate=yes;"
)

cursor = conn.cursor()

@app.route("/Fcadastro", methods=["POST"])
def fcadastro():
    nome = request.form["nome"]
    email = request.form["email"]
    fone = request.form["fone"]
    curso = request.form["curso"]
    serie = request.form["serie"]
    senha = request.form["senha"]
    
    cursor.execute(
        "insert into usuario (nome, email, fone, senha, curso, serie) values (?, ?, ?, ?, ?, ?)",
        (nome, email, fone, senha, curso, serie)
    )
    conn.commit()
    
    return "cadastrado"
    
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/ligas")
def ligas():
    return render_template("ligas.html")

if __name__ == "__main__":
    app.run(debug=True)
    