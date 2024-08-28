from telebot.types import ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove
from dotenv import load_dotenv
import telebot, os, threading

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help', 'ayuda'])
def cmd_start(message):
    bot.send_message(
        message.chat.id, 
        "Usa /alta para introducir datos",
        reply_markup=ReplyKeyboardRemove(),
    )
  
    
@bot.message_handler(commands=['alta'])
def cmd_alta(message):
    msg = bot.send_message(
        message.chat.id, 
        "Como te llamas?", 
        reply_markup=ForceReply(),
    )
    bot.register_next_step_handler(msg, recibir_nombre)
    
    
def recibir_nombre(message):
    nombre = message.text
    
    #guardar nombre en BD
    
    msg = bot.send_message(
        message.chat.id, 
        f"Bien, ahora dime tu edad. {nombre}",
        reply_markup=ForceReply(),
    )
    bot.register_next_step_handler(msg, recibir_edad)
    
    
def recibir_edad(message):
    edad = message.text
    if not edad.isdigit():
        msg = bot.send_message(
            message.chat.id, 
            "Error, debes indicar un número.\n Cuantos años tienes?",
            reply_markup=ForceReply(),
        )
        bot.register_next_step_handler(msg, recibir_edad)
    else:   
        #guardar edad en BD
        
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True,
        )
        
        markup.add('Hombre', 'Mujer')
        
        msg = bot.send_message(
            message.chat.id, 
            "Registrado, seleccione su sexo",
            reply_markup=markup,
        )
        
        bot.register_next_step_handler(msg, recibir_sexo)
        

def recibir_sexo(message):
    sexo = message.text
    if sexo.lower() not in ['hombre', 'mujer']:
        markup = ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un boton",
            resize_keyboard=True,
        )
        
        markup.add('Hombre', 'Mujer')
        
        msg = bot.send_message(
            message.chat.id, 
            f"Error, seleccione Hombre o Mujer.",
            reply_markup=markup,
        )
        bot.register_next_step_handler(msg, recibir_sexo)
    else:
        bot.send_message(
            message.chat.id, 
            "Registrado, gracias por la información.",
            reply_markup=ReplyKeyboardRemove(),
        )
    
    
if __name__ == "__main__":
    print("Iniciando Bot...")
    bot.infinity_polling()