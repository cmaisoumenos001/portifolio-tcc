from flask import Flask, render_template, request, url_for, session, redirect, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import pyodbc
import os

app = Flask("__name__")
app.secret_key = "C_Mais_Ou_Menos_1972"
app.permanent_session_lifetime = timedelta(days=7)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "txt"}

def permitido(nome):
    return "." in nome and nome.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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
    
    senha_hash = generate_password_hash(senha)
    
    cursor.execute(
        "insert into usuario (nome, email, fone, senha, curso, serie) values (?, ?, ?, ?, ?, ?)",
        (nome, email, fone, senha_hash, curso, serie)
    )
    conn.commit()
    
    return render_template("login.html")
    



@app.route("/flogin", methods=["POST"])
def flogin():
    email = request.form["email"]
    senha = request.form["senha"]
    
    cursor.execute(
        "select id_user, senha from usuario where email = ?",
        (email,)
    )
    user = cursor.fetchone()
    
    if user and check_password_hash(user[1], senha):
        session["id_user"] = user[0]
        return redirect(url_for("home"))
    else:
        return "login invalido"
    
    

 
    
@app.route("/Fliga", methods=["POST"])
def fliga():
    liga = request.form["liga"]
    valor = request.form["valor"]
    admin = request.form["nocr"]
    datai = request.form["datai"].replace("T", " ")
    fechamento = request.form["fechamento"].replace("T", " ")
    desc = request.form["dscr"]
    tipo = request.form["tipo"]
    
    arquivo = request.files.get("regras")
    caminho = None

    if arquivo and permitido(arquivo.filename):
        nome_arquivo = secure_filename(arquivo.filename)
        caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
        arquivo.save(caminho)
    
    cursor.execute(
        "insert into ligas (nome_da_liga, valor, adm_liga, data_criacao, descricao, fec_pag, tipo, regras) values (?, ?, ?, ?, ?, ?, ?, ?)",
        (liga, valor, admin, datai, desc, fechamento, tipo, caminho)
    )
    conn.commit()
    
    return render_template("index.html")   
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 
    
    
    
@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    
    return redirect(url_for("login"))
    

@app.route("/")
def home():
    nome = None

    if "id_user" in session:
        cursor.execute(
            "select nome from usuario where id_user = ?",
            (session["id_user"],)
        )
        user = cursor.fetchone()   
        nome = user[0]     
    
    return render_template("index.html", nome=nome)

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
    
