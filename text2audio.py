#the following code uses elevenlabs to convert text to audi.
#here it uses multilingual model to convert sanskrit text to voice and saves it in a audio file
import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/sY2peC9GbHX8NCy5enOe" #prem

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "enter u api_key"
}

data = {
  "text": "देवदत्त ओदनं पचति। देवदत्त ओदनं पचते। अथ प्रथमो ऽध्यायः राम एव लक्ष्मणस्य भ्राता",
  "model_id": "eleven_multilingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output5.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
