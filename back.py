from flask import Flask, render_template, request, url_for, session, redirect
import pyodbc


app = Flask("__name__")
app.secret_key = "C_Mais_Ou_Menos_1972"


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
    
    return render_template("login.html")
    
@app.route("/Fliga", methods=["POST"])
def fliga():
    liga = request.form["liga"]
    valor = request.form["valor"]
    admin = request.form["nocr"]
    datai = request.form["datai"].replace("T", " ")
    fechamento = request.form["fechamento"].replace("T", " ")
    desc = request.form["dscr"]
    tipo = request.form["tipo"]
    
    cursor.execute(
        "insert into ligas (nome_da_liga, valor, adm_liga, data_criacao, descricao, fec_pag, tipo) values (?, ?, ?, ?, ?, ?, ?)",
        (liga, valor, admin, datai, desc, fechamento, tipo)
    )
    conn.commit()
    
    return render_template("index.html")


@app.route("/flogin", methods=["POST"])
def flogin():
    email = request.form["email"]
    senha = request.form["senha"]
    
    cursor.execute(
        "select id_user, senha from usuario where email = ?",
        (email,)
    )
    user = cursor.fetchone()
    
    if user and user[1] == senha:
        session["id_user"] = user[0]
        return redirect(url_for("home"))
    else:
        return "login invalido"
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    