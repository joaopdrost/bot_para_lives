import webbrowser
from obswebsocket import obsws, requests
from flask import Flask, render_template, request
import threading
import time
import os  # Importar a biblioteca os

app = Flask(__name__)

# Configurações do OBS
host = 'localhost'
port = 4444
password = 'sua_senha'  # Defina a senha que você configurou no OBS

# Conectar ao OBS
ws = obsws(host, port, password)
ws.connect()

def start_recording():
    ws.call(requests.StartRecording())

def stop_recording():
    ws.call(requests.StopRecording())

def open_youtube_live(url):
    webbrowser.open(url)

def split_record_file():
    ws.call(requests.StopRecording())
    time.sleep(1)  # Aguarda um segundo antes de iniciar a nova gravação
    ws.call(requests.StartRecording())
    print("Gravação dividida.")

def main(url, duration):
    open_youtube_live(url)  # Abre a URL da live
    
    start_recording()  # Inicia a gravação
    print("Gravação iniciada.")
    while True:
        # Aguarda a duração especificada (em segundos)
        time.sleep(duration)
        print("Dividindo a gravação em um novo arquivo")
        split_record_file()

def run_bot(url, duration):
    main(url, duration)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        hours = int(request.form['hours'])  # Captura horas
        minutes = int(request.form['minutes'])  # Captura minutos
        seconds = int(request.form['seconds'])  # Captura segundos
        
        # Converte tudo para segundos
        duration = hours * 3600 + minutes * 60 + seconds
        
        # Iniciar o bot em uma nova thread
        threading.Thread(target=run_bot, args=(url, duration)).start()
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use a porta fornecida pelo Heroku ou 5000 localmente
    app.run(host='0.0.0.0', port=port, debug=True)