from flask import Flask, render_template, request, jsonify
import threading
import sounddevice as sd
from .gen_ai_logic.answer_back import ask_openai
from .sounding.voice_the_text import play_audio, voice_the_text
from .audio_utils.convertions import get_text_from_audio

app = Flask(__name__)

recording = []
is_recording = False
sample_rate = 44100
loading = False

def start_recording():
    global is_recording, recording
    recording = []  # Инициализация массива для хранения записанных данных

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
        while is_recording:
            data = stream.read(sample_rate // 10)[0]  # Читаем 100 мс аудиоданных
            recording.append(data.copy())  # Добавляем данные в массив

@app.route('/')
def index():
    return render_template('index.html')  # Отображение HTML-интерфейса

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    assistant_response = ask_openai(user_message)
    audio_stream, duration = voice_the_text(assistant_response)

    # Запуск аудио в отдельном потоке
    threading.Thread(target=play_audio, args=(audio_stream,)).start()

    return jsonify({"response": assistant_response})

@app.route('/start_recording', methods=['POST'])
def start_audio_recording():
    global is_recording
    is_recording = True
    threading.Thread(target=start_recording).start()
    return jsonify({"status": "recording started"})

@app.route('/stop_recording', methods=['POST'])
def stop_audio_recording():
    global is_recording
    is_recording = False
    text_message = get_text_from_audio(recording)
    return jsonify({"text": text_message})

if __name__ == '__main__':
    app.run(debug=True)
