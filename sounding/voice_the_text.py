from gtts import gTTS
from io import BytesIO
import pygame
from mutagen.mp3 import MP3
from langdetect import detect, DetectorFactory

# Устанавливаем фиксированное семя для детектора, чтобы обеспечить детерминированность
DetectorFactory.seed = 0

def voice_the_text(text):
    # Определяем язык текста
    lang = detect(text)
    
    # Устанавливаем язык для gTTS
    if lang == 'ru':
        tts = gTTS(text=text, lang='ru', slow=False)
    elif lang == 'en':
        tts = gTTS(text=text, lang='en', slow=False)
    else:
        raise ValueError("Unsupported language detected.")

    audio_stream = BytesIO()
    tts.write_to_fp(audio_stream)

    audio_stream.seek(0)
    audio = MP3(audio_stream)
    duration = audio.info.length
    return audio_stream, duration

def play_audio(audio_stream):
    pygame.mixer.init()
    audio_stream.seek(0)
    pygame.mixer.music.load(audio_stream, 'mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.stop()
    pygame.mixer.quit()

if __name__ == "__main__":
    text = "What the hell you just said ?"
    audio_stream, duration = voice_the_text(text)
    play_audio(audio_stream)
