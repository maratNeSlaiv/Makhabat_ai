import time
import io
import wave
import numpy as np
from app.gen_ai_logic.answer_back import convert_audio_to_text

sample_rate = 44100

def save_to_wav_bytes(recording):
    wav_bytes = io.BytesIO()
    with wave.open(wav_bytes, 'wb') as wf:
        wf.setnchannels(1)  # Одноканальный (моно)
        wf.setsampwidth(2)  # 16 бит = 2 байта
        wf.setframerate(sample_rate)
        wf.writeframes(np.concatenate(recording).tobytes())  # Объединяем буферы
    wav_bytes.seek(0)  # Перемещаем указатель в начало
    return wav_bytes

def get_text_from_audio(recording):
    print("Запись остановлена.")
    audio_file = save_to_wav_bytes(recording)
    audio_file.name = "recording.wav"
    
    text_message = convert_audio_to_text(audio_file)
    return text_message

if __name__ == '__main__':
    from openai import OpenAI
    client = OpenAI()

    filename = '/Users/maratorozaliev/Desktop/goodto.m4a'
    audio_file= open(filename, "rb")
    start_time = time.time()
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format='text'
    )
    end_time = time.time()
    print(transcription)
    print('Difference:', end_time - start_time)