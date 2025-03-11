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

def main(url, duration):
    open_youtube_live(url)  # Abre a URL da live
    
    while True:
        start_recording()  # Inicia a gravação
        print("Gravação iniciada.")
        
        # Aguarda a duração especificada (em segundos)
        time.sleep(duration)
        
        stop_recording()  # Para a gravação
        print("Gravação parada.")
        
        # Reinicia a gravação imediatamente após o tempo de gravação
        print("Reiniciando a gravação...")

       
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
    app.run(debug=True)
