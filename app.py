from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import smtplib
from email.mime.text import MIMEText
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados SQLite
def criar_tabela_usuarios():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Criar tabela de usuários se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Chama a função para criar a tabela no início do aplicativo
criar_tabela_usuarios()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir arquivos estáticos do diretório "static"
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Lógica para verificar as credenciais no banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            # Usuário autenticado com sucesso, redirecione para o dashboard
            return redirect(url_for('user'))
        else:
            # Credenciais inválidas, exiba uma mensagem de erro
            return render_template('cadastro.html', error='Credenciais inválidas. Tente novamente.')

    # Se a solicitação for do tipo GET, renderize a página de login
    return render_template('cadastro.html')

# Rota para o dashboard (página do usuário)
@app.route('/user')
def user():
    # Lógica para processar a página do usuário
    return render_template('user.html')

# Rota para a página de cadastro
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Adiciona lógica para salvar os dados na tabela de usuários
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))

        conn.commit()
        conn.close()

        # Enviar e-mail de confirmação
        assunto = 'Confirmação de Cadastro'
        mensagem = f'Olá {nome}, obrigado por se cadastrar!\nSeu e-mail é {email} e sua senha é {senha}.'

        erro_envio_email = enviar_email(email, assunto, mensagem)

        if erro_envio_email:
            return f"Erro ao enviar e-mail: {erro_envio_email}"

        # Redirecionar para a página inicial ou uma página de confirmação
        return render_template('user.html')

    # Se a solicitação for do tipo GET, renderize a página de cadastro
    return render_template('cadastro.html')

# Rota para o calendário
@app.route('/calendario')
def calendario():
    return render_template('calend.html')

# Rotas adicionadas com caminhos únicos
@app.route('/iniciar')
def iniciar():
    return render_template('iniciar.html')

@app.route('/notas')
def notas():
    return render_template('notas.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

# Função para enviar e-mails
def enviar_email(destinatario, assunto, mensagem):
    remetente = 'financaflex@gmail.com'  # Substitua pelo seu e-mail
    senha = 'wlwy ozez twni fjhm'

    try:
        # Lógica para enviar e-mail usando o módulo smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)

        msg = MIMEText(mensagem)
        msg['Subject'] = assunto
        msg['From'] = remetente
        msg['To'] = destinatario

        server.sendmail(remetente, destinatario, msg.as_string())
        return None  # Nenhum erro, e-mail enviado com sucesso
    except smtplib.SMTPAuthenticationError as e:
        return f"Erro de autenticação SMTP: {e}"
    except smtplib.SMTPException as e:
        return f"Erro SMTP: {e}"
    finally:
        server.quit()

# Função principal para executar o aplicativo
if __name__ == '__main__':
    app.run(debug=True)
