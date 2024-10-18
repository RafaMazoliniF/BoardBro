import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configurações para o upload de arquivos
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')  # Diretório onde os arquivos serão salvos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limitar o tamanho do upload (ex: 16MB)

# Rota principal para exibir o formulário
@app.route("/")
def home():
    return render_template('home.html')

# Rota para fazer o upload do arquivo
@app.route("/upload", methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return "Nenhum arquivo foi enviado", 400

    file = request.files['pdf']

    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    if file and file.filename.endswith('.pdf'):
        # Salva o arquivo na pasta /data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return f"Arquivo {file.filename} salvo com sucesso em {file_path}"
    else:
        return "Por favor, envie um arquivo PDF", 400

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # Cria a pasta /data se ela não existir
    app.run(debug=True)
