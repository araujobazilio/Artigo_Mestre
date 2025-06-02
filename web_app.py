from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
from crew_logic import create_crew, save_articles
import os
import threading
import webbrowser
import json

app = Flask(__name__)
Bootstrap(app)

# Limpar progresso anterior
def clear_progress():
    progress_file = os.path.join('static', 'progress.json')
    if os.path.exists(progress_file):
        os.remove(progress_file)

@app.route('/')
def index():
    clear_progress()
    return render_template('index.html')

@app.route('/gerar_artigos', methods=['POST'])
def gerar_artigos():
    topico = request.form['topico']
    
    # Limpar progresso anterior
    clear_progress()
    
    # Criar e executar o crew em uma thread separada
    def run_crew():
        # Criar e executar o crew
        crew = create_crew(topico)
        result = crew.kickoff(inputs={"tópico": topico})
        
        # Salvar artigos
        filename = save_articles(topico, result)
        
        # Salvar nome do arquivo para download
        with open(os.path.join('static', 'last_article.txt'), 'w') as f:
            f.write(filename)
    
    # Iniciar crew em thread separada
    threading.Thread(target=run_crew, daemon=True).start()
    
    return render_template('processando.html', topico=topico)

@app.route('/progresso')
def progresso():
    progress_file = os.path.join('static', 'progress.json')
    try:
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        return jsonify(progress)
    except FileNotFoundError:
        return jsonify([])

@app.route('/status_artigo')
def status_artigo():
    try:
        with open(os.path.join('static', 'last_article.txt'), 'r') as f:
            filename = f.read().strip()
        return jsonify({'status': 'concluido', 'filename': filename})
    except FileNotFoundError:
        return jsonify({'status': 'processando'})

@app.route('/download_artigo/<filename>')
def download_artigo(filename):
    return send_from_directory('static/artigos', filename, as_attachment=True)

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('static/artigos', exist_ok=True)
    
    # Agendar a abertura do navegador
    threading.Timer(1.5, open_browser).start()
    
    # Iniciar o servidor Flask
    app.run(debug=True)
