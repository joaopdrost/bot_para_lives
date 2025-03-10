import webbrowser
from obswebsocket import obsws, requests
from flask import Flask, render_template, request
import threading
import time

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

def main(url):
    open_youtube_live(url)  # Abre a URL da live
    while True:
        start_recording()  # Inicia a gravação
        print("Gravação iniciada.")
        
        # Aguarda 30 minutos (em segundos)
        time.sleep(10)  # Gravação de 30 minutos
        
        stop_recording()  # Para a gravação
        print("Gravação parada.")
        
        # Espera 1 milissegundo antes de reiniciar
        time.sleep(0.001)  # Espera 1 milissegundo
        
        print("Reiniciando a gravação...")

def run_bot(url):
    main(url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # Iniciar o bot em uma nova thread
        threading.Thread(target=run_bot, args=(url,)).start()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)