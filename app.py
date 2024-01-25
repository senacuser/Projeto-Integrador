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

# Rota para a página de recuperação de senha
@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']

        # Lógica para verificar se o e-mail existe no banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            # Se o e-mail existe, redirecione para a página de redefinição de senha
            return redirect(url_for('redefinir_senha', email=email))
        else:
            # Se o e-mail não existe, exiba uma mensagem de erro
            return render_template('recuperar_senha.html', error='E-mail não encontrado. Verifique o e-mail e tente novamente.')

    # Se a solicitação for do tipo GET, renderize a página de recuperação de senha
    return render_template('recuperar_senha.html')

# Rota para a página de redefinição de senha
@app.route('/redefinir_senha/<email>', methods=['GET', 'POST'])
def redefinir_senha(email):
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']

        # Lógica para atualizar a senha no banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE usuarios SET senha = ? WHERE email = ?", (nova_senha, email))

        conn.commit()
        conn.close()

        # Redirecionar para a página de login após a redefinição da senha
        return redirect(url_for('login'))

    # Se a solicitação for do tipo GET, renderize a página de redefinição de senha
    return render_template('redefinir_senha.html', email=email)

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


# Configuração do banco de dados SQLite
def criar_tabela_transacoes():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Criar tabela de transações se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    conn.commit()
    conn.close()

# Chama a função para criar a tabela de transações no início do aplicativo
criar_tabela_transacoes()
@app.route('/controle', methods=['POST', 'GET'])
def controle():
    if request.method == 'POST':
        nome = request.form['nome']
        valor = float(request.form['valor'])
        tipo = request.form['tipo']

        # Adicionar lógica para salvar as transações no banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO transacoes (usuario_id, nome, valor, tipo) VALUES (?, ?, ?, ?)",
                       (4, nome, valor if tipo == 'Entrada' else -valor, tipo))  

        conn.commit()
        conn.close()

    return render_template('controle.html')

# Rota para o dashboard (página do usuário)
@app.route('/dashboard')
def dashboard():
    # Lógica para processar a página do dashboard
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Recuperar transações do banco de dados
    cursor.execute("SELECT * FROM transacoes WHERE usuario_id = ?", (4,))  # Substitua 1 pelo ID do usuário logado
    transacoes = cursor.fetchall()

    conn.close()

    # Calcular valores
    salario = sum(transacao[2] for transacao in transacoes if transacao[3] == 'Salario')
    entradas = sum(transacao[2] for transacao in transacoes if transacao[3] == 'Entrada')
    saidas = sum(transacao[2] for transacao in transacoes if transacao[3] == 'Saida')
    valor_total = entradas - saidas

    return render_template('dashboard.html', salario=salario, entradas=entradas, saidas=saidas, valor_total=valor_total) 

# Rota para a página de controle de despesas

# Rota para o calendário
@app.route('/calendario')
def calendario():
    return render_template('calendario.html')
@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/solucoes')
def solucoes():
    return render_template('solucoes.html')

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