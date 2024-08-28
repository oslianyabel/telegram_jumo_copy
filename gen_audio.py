from gtts import gTTS

# Texto a convertir en audio
texto = "Hola mundo desde Cuba"

# Genera el archivo de audio
tts = gTTS(text=texto, lang='es')
tts.save("hola_mundo_desde_cuba.mp3")
