from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# modelo do banco
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    ensino = db.Column(db.String(50))

# criar banco
with app.app_context():
    db.create_all()

# página principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        cpf = request.form["cpf"]

        # 🔍 Verifica se já existe no banco
        usuario = Usuario.query.filter_by(cpf=cpf).first()

        if usuario:
            # ✅ Se existe → vai pro certificado
            return redirect(url_for("certificado", id=usuario.id))
        else:
            # ❌ Se NÃO existe → recusa
            return render_template("recusado.html")

    return render_template("index.html")

# página certificado
@app.route("/certificado/<int:id>")
def certificado(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template("certificado.html", usuario=usuario)

if __name__ == "__main__":
    app.run(debug=True)