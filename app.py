from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import smtplib
from email.mime.text import MIMEText
import mysql.connector
app = Flask(__name__)

# Configuração do banco de dados
#db = mysql.connector.connect(
#    host="seu_host",
#    user="seu_usuario",
#    password="sua_senha",
#    database="seu_banco_de_dados"
#)

@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir arquivos estáticos do diretório "main"
@app.route('/main/<path:filename>')
def serve_static(filename):
    return send_from_directory('main', filename)

# rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticação aqui
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# rota para o dashboard
@app.route('/dashboard')
def dashboard():
    # Lógica para recuperar dados do banco e criar dashboards
    return render_template('dashboard.html')

#Cadastro e confirmação de email
@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Aqui você pode adicionar lógica para salvar os dados em um banco de dados, se necessário.

        # Enviar e-mail de confirmação
        assunto = 'Confirmação de Cadastro'
        mensagem = f'Olá {nome}\n\
        obrigado por se cadastrar!\n\
        Seu e-mail é {email}\n\
        e sua senha é {senha}.'

        erro_envio_email = enviar_email(email, assunto, mensagem)

        if erro_envio_email:
            return f"Erro ao enviar e-mail: {erro_envio_email}"

        # Redirecionar para a página inicial ou uma página de confirmação
        return render_template('user.html')


    # Se a solicitação for do tipo GET, renderize a página de cadastro
    return render_template('cadastro.html')

@app.route('/calendario')
def calendario():
    return render_template('calend.html')

def enviar_email(destinatario, assunto, mensagem):
    remetente = 'financaflex@gmail.com'  # Substitua pelo seu e-mail
    senha = 'wlwy ozez twni fjhm'

    try:
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

if __name__ == '__main__':
    app.run(debug=True)
