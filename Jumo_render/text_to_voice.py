from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

speech_file_path = Path(__file__).parent / "voice_examples/shimmer.mp3"
response = client.audio.speech.create(
  model="tts-1-hd",
  voice="shimmer",
  input="Hola, que le parece mi nueva voz. Recuerde que estoy aqui para ayudarle, sobre que le interesa hablar?"
)
response.stream_to_file(speech_file_path)