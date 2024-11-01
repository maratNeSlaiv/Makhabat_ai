import io
import wave
import numpy as np
from gen_ai_logic.answer_back import convert_audio_to_text

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