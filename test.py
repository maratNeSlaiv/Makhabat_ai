import tkinter as tk
import pyaudio
import wave
import threading

# Global variables to manage recording state
is_recording = False
frames = []

# Function to record audio
def record_audio():
    global is_recording, frames
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)
    
    frames = []  # Clear any previous frames
    while is_recording:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save recorded audio to a WAV file
    with wave.open("recorded_audio.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

# Function to start recording
def start_recording():
    global is_recording
    is_recording = True
    threading.Thread(target=record_audio, daemon=True).start()
    record_button.config(text="Release to Stop")

# Function to stop recording
def stop_recording(event=None):
    global is_recording
    is_recording = False
    record_button.config(text="Press to Record")

# Create the GUI window
root = tk.Tk()
root.title("Voice Recorder")
root.geometry("300x150")

# Create a button to record audio
record_button = tk.Button(root, text="Press to Record", width=20, height=2, bg="lightblue")
record_button.pack(pady=50)

# Bind the start/stop recording to the button
record_button.bind("<ButtonPress-1>", lambda event: start_recording())
record_button.bind("<ButtonRelease-1>", stop_recording)

# Run the GUI
root.mainloop()
