import os 
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

system_params = {
    "temperature": 0.7,
    "frequency_penalty": 0.5,
    "presence_penalty": 0.6
}

conversation_history = [{"role": "system", "content": "Ты — помощник, который отвечает кратко и по делу."}]
conversation_history = []
def ask_openai(question):
    global conversation_history
    conversation_history.append({"role": "user", "content": question})

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        **system_params
    )
    answer = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": answer})
    return answer


######## 
"AUDIO"
########
def convert_audio_to_text(audio_in_wav_bytes):
    client = OpenAI()
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_in_wav_bytes
    )
    return transcription.text
