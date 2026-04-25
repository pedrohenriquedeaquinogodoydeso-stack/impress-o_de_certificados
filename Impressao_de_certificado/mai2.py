# VVVVVVImportar
from flask import Flask, render_template, request, redirect, url_for
# VVVVVVVImportando a biblioteca de banco de dados
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
# VVVVVVVVVVVVVConectando ao SQLite

# Função para conectar ao banco diary.db
def init_db():
    conn = sqlite3.connect('diary.db')
    cursor = conn.cursor()
    # Cria a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            time_escolhido TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@app.route('/cadastro/<nome_time>')
def pagina_cadastro(nome_time):
    # Renderiza uma página de formulário simples
    return render_template('form_cadastro.html', time=nome_time)

@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form.get('nome')
    time = request.form.get('time')

    if nome and time:
        conn = sqlite3.connect('instance/diary.db') # Verifique se o caminho está correto
        cursor = conn.cursor()
        
        # Alterado de 'jogadores' para 'card'
        # E usando as colunas que você tem: title (nome) e subtitle (time)
        cursor.execute("INSERT INTO card (title, subtitle, text) VALUES (?, ?, ?)", 
                       (nome, time, "Inscrição confirmada!"))
        
        conn.commit()
        conn.close()
        return redirect('/') 
    
    return "Erro: Nome ou Time não fornecidos."



#AAAAAAAAAAAAAAAaaaaaaaaaaaaaaaaaaaaaaaaaaa

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# VVVVVVVVVVVVVVCriando um Banco de Dados (DB)
db = SQLAlchemy(app)

#VVVVVVVVVVVVV Tarefa #1. Criar uma tabela no Banco de Dados

class Card(db.Model):
    __tablename__ = 'card' # Garante que ele use a tabela que você já criou
    id = db.Column(db.Integer, primary_key=True) # O segredo está aqui!
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(500), nullable=False)

    

@app.route('/times')
def listar_times():
    conn = sqlite3.connect('instance/diary.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Busca todos os registros da tabela card
    jogadores = cursor.execute('SELECT * FROM card').fetchall()
    conn.close()
    
    # Definimos a lista oficial dos times da Liga Neo Egoísta
    lista_times = ['ubers', 'manshine', 'barcha', 'pxg', 'bastard']
    
    return render_template('times.html', jogadores=jogadores, times=lista_times)








# VVVVVVVVVVVVExecutando a página com conteúdo
@app.route('/')

def escolha():
    

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)