from telebot.types import ReplyKeyboardRemove
from dotenv import load_dotenv
from openai import OpenAI
import os, telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BIBLE_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def text_to_voice(text, voice, chat_id):
    bot.send_chat_action(chat_id, "record_audio")
    response = client.audio.speech.create(
        model = "tts-1",
        voice = voice,
        input = text
    )
    response.stream_to_file("voice_out.mp3")
    return "voice_out.mp3"

def voice_to_text(message):
    # Descargar el archivo de audio
    file_info = bot.get_file(message.audio.file_id if message.audio else message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Guardar el archivo en local
    with open("voice_in.mp3", 'wb') as audio_file:
        audio_file.write(downloaded_file)
        print("Audio recibido y guardado.")
        
    with open("voice_in.mp3", 'rb') as audio_file:
        #transcripcion
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        print(f"Transcripción del audio: {transcription.text}")
        
    return transcription.text
    

def send_message(message, text, voice_msg_activated, voice):
    try:
        x = voice[message.chat.id]
    except KeyError as e:
        voice[message.chat.id] = "alloy"
        
    try:
        y = voice_msg_activated[message.chat.id]
    except KeyError as e:
        voice_msg_activated[message.chat.id] = False
        
    if voice_msg_activated[message.chat.id]:
        try:
            voice_path = text_to_voice(text, voice[message.chat.id], message.chat.id)
            with open(voice_path, 'rb') as audio:
                bot.send_chat_action(message.chat.id, "upload_audio")
                bot.send_voice(message.chat.id, audio, reply_markup=ReplyKeyboardRemove(), timeout=60)
        except Exception as e:
            print(e)
            bot.send_chat_action(message.chat.id, "typing")
            msg = "Lo siento, el envío del audio ha fallado. Le responderé esta vez con texto."
            bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(message.chat.id, text)
    else:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove())
        