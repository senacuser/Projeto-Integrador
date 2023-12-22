from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telaprincipal')
def telaprincipal():
    return render_template('user.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/calendario')
def calendario():
    return render_template('calend.html')

if __name__ == '__main__':
    app.run(debug=True)
