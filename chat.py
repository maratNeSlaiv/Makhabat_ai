import tkinter as tk
import threading
import time
import sounddevice as sd
from gen_ai_logic.answer_back import ask_openai
from sounding.voice_the_text import play_audio, voice_the_text
from audio_utils.convertions import get_text_from_audio

recording = None
is_recording = False
sample_rate = 44100
loading = False

def start_recording():
    global is_recording, recording
    print("Начинаю запись...")
    recording = []  # Инициализация массива для хранения записанных данных

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
        while is_recording:
            data = stream.read(sample_rate // 10)[0]  # Читаем 100 мс аудиоданных
            recording.append(data.copy())  # Добавляем данные в массив

def send_message(user_message):
    global loading
    if user_message:
        chat_window.insert(tk.END, "Вы: " + user_message + "\n")
        user_input.delete(0, tk.END)
        loading = True
        chat_window.insert(tk.END, "Алгоритм: ")
        threading.Thread(target=draw_loading_points).start()
        threading.Thread(target=get_response, args=(user_message,)).start()

def record_audio():
    global is_recording
    is_recording = True
    threading.Thread(target=start_recording).start()

def stop_audio_recording():
    global is_recording
    if is_recording:
        is_recording = False
        text_message = get_text_from_audio(recording)
        if text_message:
            send_message(text_message)

def draw_loading_points():
    loading_text = ""
    while loading:
        for i in range(1, 6):
            if not loading:
                break
            loading_text = "." * i
            chat_window.delete("end-2l", tk.END)
            chat_window.insert(tk.END, "Алгоритм: " + loading_text)
            time.sleep(0.3)

def get_response(user_message):
    global loading
    assistant_response = ask_openai(user_message)
    loading = False
    audio_stream, duration = voice_the_text(assistant_response)
    chat_window.delete("end-2l", tk.END)

    play_audio_thread = threading.Thread(target=play_audio, args=(audio_stream,))
    play_audio_thread.start()

    # Разделяем ответ на фрагменты
    words = assistant_response.split()
    word_count = len(words)
    delay = duration / word_count if word_count > 0 else 0  # Время задержки между словами

    for word in words:
        chat_window.insert(tk.END, word + ' ')
        chat_window.see(tk.END)  # Прокручиваем текстовое окно вниз
        time.sleep(delay)  # Задержка перед выводом следующего слова

    chat_window.insert(tk.END, "\n")  # Перевод строки после завершения

def main_event():
    global chat_window, user_input
    root = tk.Tk()
    root.title("Простой Чат")

    chat_window = tk.Text(root, width=70, height=30, bg="lightyellow", font=("Arial", 12))
    chat_window.pack(padx=10, pady=5)

    input_label = tk.Label(root, text="Введите сообщение:", font=("Arial", 12))
    input_label.pack(padx=10, pady=5)

    user_input = tk.Entry(root, width=40)
    user_input.pack(padx=10, pady=5)

    send_button = tk.Button(root, text="Отправить", command=lambda: send_message(user_input.get()))
    send_button.pack(pady=5)

    record_button = tk.Button(root, text="Запись аудио", command=lambda: None,
                            bg="skyblue", fg="black", font=("Arial", 12, "bold"),
                            relief="raised", padx=10, pady=5)

    record_button.pack(pady=5)

    # Bind events to start and stop recording
    record_button.bind('<ButtonPress>', lambda event: record_audio())
    record_button.bind('<ButtonRelease>', lambda event: stop_audio_recording())

    root.mainloop()

if __name__ == '__main__':
    main_event()