from flask import Flask, render_template, request, url_for, session, redirect, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pyodbc
import os

app = Flask("__name__")
app.secret_key = "C_Mais_Ou_Menos_1972"
app.permanent_session_lifetime = timedelta(days=7)


app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="cmaisoumenos001@gmail.com",
    MAIL_PASSWORD="rlqq ycij btko rmho"
)

mail = Mail(app)
s = URLSafeTimedSerializer(app.secret_key)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "txt"}

def permitido(nome):
    return "." in nome and nome.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


conn = pyodbc.connect(
    "driver={ODBC Driver 18 for SQL Server};server=localhost;database=tcc;trusted_connection=yes;trustservercertificate=yes;"
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

    cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
    existe = cursor.fetchone()

    if existe:
        return render_template("cadastro.html", erro="Email já cadastrado")

    cursor.execute(
        "INSERT INTO usuario (nome, email, fone, senha, curso, serie, ativo) VALUES (?, ?, ?, ?, ?, ?, 0)",
        (nome, email, fone, senha_hash, curso, serie)
    )
    conn.commit()

    token = s.dumps(email, salt="email-confirm")
    link = f"http://192.168.1.8:5000/confirmar/{token}"

    msg = Message("Confirme seu email", sender="seuemail@gmail.com", recipients=[email])
    msg.body = f"Clica aqui pra ativar tua conta: {link}"

    mail.send(msg)

    return redirect(url_for("login"))



@app.route("/flogin", methods=["POST"])
def flogin():
    email = request.form["email"]
    senha = request.form["senha"]

    cursor.execute(
        "SELECT id_user, senha, ativo FROM usuario WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    if user and check_password_hash(user[1], senha):

        if not user[2]:
            return render_template("login.html", erro="Confirme seu email")

        session["id_user"] = user[0]
        return redirect(url_for("home"))

    return render_template("login.html", erro="Email ou senha inválidos")
    
@app.route("/Fliga", methods=["POST"])
def fliga():
    liga = request.form["liga"]
    valor = request.form["valor"]
    datai = request.form["datai"].replace("T", " ")
    fechamento = request.form["fechamento"].replace("T", " ")
    desc = request.form["dscr"]
    tipo = request.form["Tipo"]
    
    arquivo = request.files.get("regras")
    caminho = None
    
    
    id_user = session.get("id_user")

    cursor.execute(
        "SELECT nome FROM usuario WHERE id_user = ?",
        (id_user,)
    )
    user = cursor.fetchone()

    admin = user[0] if user else None
    
    if arquivo and permitido(arquivo.filename):
        nome_arquivo = secure_filename(arquivo.filename)
        caminho = os.path.join(app.config["UPLOAD_FOLDER"], nome_arquivo)
        arquivo.save(caminho)
    
    cursor.execute(
        "insert into ligas (nome_da_liga, valor, adm_liga, data_criacao, descricao, fec_pag, tipo, regras) values (?, ?, ?, ?, ?, ?, ?, ?)",
        (liga, valor, admin, datai, desc, fechamento, tipo, caminho)
    )
    conn.commit()
    
    return redirect(url_for("home"))   
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 
    
    
@app.route("/confirmar/<token>")
def confirmar_email(token):
    try:
        email = s.loads(token, salt="email-confirm", max_age=3600)
    except:
        return render_template("confirmacao.html", mensagem="Link inválido ou expirado")

    cursor.execute(
        "UPDATE usuario SET ativo = 1 WHERE email = ?",
        (email,)
    )
    conn.commit()

    return render_template("confirmacao.html", mensagem="Email confirmado com sucesso")   
    
    
    
    
    
    
@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.clear()
    
    return redirect(url_for("home"))
    

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
    
    cursor.execute("SELECT * FROM ligas")
    ligas = cursor.fetchall()

    return render_template("index.html", nome=nome, ligas=ligas)
    

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
    app.run(host="0.0.0.0", debug=True)
    
#TODO criar tela de perfil e login/perfil de integrante do gremio