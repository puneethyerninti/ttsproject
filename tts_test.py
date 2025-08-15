from gtts import gTTS

text = "Hello Puneeth, your gTTS setup is complete!"
tts = gTTS(text, lang='en')
tts.save("output.mp3")

print("✅ Audio saved as output.mp3")
