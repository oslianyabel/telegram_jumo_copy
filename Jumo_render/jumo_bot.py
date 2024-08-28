from openai import OpenAI
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import telebot, assistant, os, utils
from flask import Flask, request
from pyngrok import ngrok, conf
from waitress import serve
import time

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
web_server = Flask(__name__)
voice_msg_activated = {}
voice = {}

@bot.message_handler(func=lambda message: message.text.startswith("@Bible01_bot"))
def handle_message(message):
    sms = f"El usuario {message.from_user.username} te ha mencionado en un grupo de telegram al que perteneces con el siguiente mensaje: {message.text[12:]}"
    
    print("Bot mencionado!")
    print(f"{message.from_user.username}: {message.text[12:]}")
    data = {
        "id": message.chat.id, 
        "message": sms
    }
    ans = assistant.send_message(data)
    bot.reply_to(message, ans)


@web_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200


@bot.message_handler(commands=["settings"])
def cmd_settings(message):
    print("/settings")
    
    markup = ReplyKeyboardMarkup(
        one_time_keyboard = True, 
        input_field_placeholder = "Pulsa un boton",
        resize_keyboard = True,
    )
    markup.add('Activar/Desactivar mensajes de voz', 'Cambiar voz', 'Salir')
    
    msg = bot.send_message(
        message.chat.id, 
        "Menu de configuración. Seleccione una opción:",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, settings_menu)


def settings_menu(message):
    if message.text == "Activar/Desactivar mensajes de voz":
        markup = ReplyKeyboardMarkup(
            one_time_keyboard = True, 
            input_field_placeholder = "Pulsa un boton",
            resize_keyboard = True,
        )
        markup.add('Texto', 'Voz')
        
        msg = bot.send_message(
            message.chat.id, 
            "Las respuestas del bot pueden ser mensajes de texto o de voz. Cuál es su preferencia?",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, settings_formats)
    elif message.text == "Cambiar voz":
        markup = ReplyKeyboardMarkup(
            one_time_keyboard = True, 
            input_field_placeholder = "Pulsa un boton",
            resize_keyboard = True,
        )
        markup.add('alloy', 'echo', 'fable', 'nova', 'onyx', 'shimmer')
        
        msg = bot.send_message(
            message.chat.id, 
            "A continuación las voces disponibles:",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, settings_voices)
    elif message.text == "Salir":
        utils.send_message(message, "Menú Cerrado", voice_msg_activated, voice)


def settings_formats(message):
    if message.text == "Texto":
        voice_msg_activated[message.chat.id] = False
        bot.send_message(message.chat.id, "Mensajes de voz desactivados", reply_markup=ReplyKeyboardRemove())
    elif message.text == "Voz":
        voice_msg_activated[message.chat.id] = True
        utils.send_message(message, "Mensajes de voz activados!", voice_msg_activated, voice)
    else:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard = True, 
            input_field_placeholder = "Pulsa un boton",
            resize_keyboard = True,
        )
        markup.add('Texto', 'Voz')
        
        msg = bot.send_message(
            message.chat.id, 
            "Seleccione una de ambas opciones por favor.",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, settings_formats)
    
    
def settings_voices(message):
    if message.text not in ['alloy', 'echo', 'fable', 'nova', 'onyx', 'shimmer']:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard = True, 
            input_field_placeholder = "Pulsa un boton",
            resize_keyboard = True,
        )
        markup.add('alloy', 'echo', 'fable', 'nova', 'onyx', 'shimmer')
        
        msg = bot.send_message(
            message.chat.id, 
            "Seleccione una de las opciones establecidas por favor.",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, settings_voices)
    else:
        voice[message.chat.id] = message.text
        audio = open(f'voice_examples/{message.text}.mp3', 'rb')
        bot.send_chat_action(message.chat.id, "upload_audio")
        bot.send_voice(message.chat.id, audio)
        audio.close()
    

@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    print("/start")
    data = {
        "id": message.chat.id, 
        "message": "Hola, en qué me puedes ayudar?"
    }
    ans = assistant.send_message(data)
    
    utils.send_message(message, ans, voice_msg_activated, voice)
    
@bot.message_handler(commands=["contact"])
def cmd_start(message):
    print("/contact")
    data = {
        "id": message.chat.id, 
        "message": "Envíame los enlaces de los sitios web de su empresa para visitarlos."
    }
    ans = assistant.send_message(data)
    utils.send_message(message, ans, voice_msg_activated, voice)
    
    
@bot.message_handler(content_types=['text'])
def reply_text(message):
    print(f"-User: {message.text}")
    data = {
        "id": message.chat.id, 
        "message": message.text
    }
    ans = assistant.send_message(data)
    utils.send_message(message, ans, voice_msg_activated, voice)
    
    
@bot.message_handler(content_types=["audio", "voice"])
def reply_audio(message):
    text = utils.voice_to_text(message)
     
    data = {
        "id": message.chat.id, 
        "message": text
    }
    ans = assistant.send_message(data)
    
    utils.send_message(message, ans, voice_msg_activated, voice)


if __name__ == "__main__":
    print("Iniciando Bot")
    
    """ NGROK_TOKEN = os.getenv('NGROK_TOKEN')
    conf.get_default().config_path = "./config_ngrok.yml"
    conf.get_default().region = "eu"
    ngrok.set_auth_token(NGROK_TOKEN)
    ngrok_tunel = ngrok.connect(5000, bind_tls = True)
    ngrok_url = ngrok_tunel.public_url
    print(ngrok_url)
    bot.remove_webhook()
    time.sleep(1) """
    
    bot.set_webhook(url = "https://telegram-jumo-bot.onrender.com")
    #web_server.run(host="0.0.0.0", port=5000)
    serve(web_server, host = "0.0.0.0", port = 1338)