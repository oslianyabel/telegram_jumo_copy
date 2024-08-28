from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

audio_file= open("audio.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model = "whisper-1", 
  file = audio_file,
  timeout = 60
)

print(transcription.text)
