from dotenv import load_dotenv
import os, requests, telebot

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BIBLE_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_message(data):
    #url = "http://127.0.0.1:3028/chat"
    url = "https://jumo-webchat.onrender.com/chat"
    #url = "http://51.210.112.67:3028/chat"
    
    headers = {
        "token": os.getenv('TOKEN_API')
    }
    
    response = requests.post(url, headers=headers, data=data)
    print(f"Codigo de respuesta: {response.status_code}")
    ans = response.json()

    if ans["status_code"] == 200:
        print(f"-Assistant: {ans['message']}")
        #bot.send_message(data["id"], ans["message"], reply_markup=ReplyKeyboardRemove())
        return ans["message"]
    else:
        error = f"Error {ans['status_code']}: {ans['error']}, {ans['message']}"
        print(error)
        #bot.send_message(data["id"], error)
        return error