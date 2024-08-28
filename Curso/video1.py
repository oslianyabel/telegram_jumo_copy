from dotenv import load_dotenv
import telebot, os, threading

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    bot.reply_to(message, "Holaa")
    
@bot.message_handler(content_types=['text'])
def reply_text(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "Comando no disponible")
    else:  
        bot.send_message(message.chat.id, "Blablabla")
    

def run_bot():
    bot.infinity_polling()

if __name__ =='__main__':
    print("Starting bot.")
    bot_thread = threading.Thread(name = 'bot_thread', target=run_bot)
    bot_thread.start()
    print("bot ready!")
