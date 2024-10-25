import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/ur required api"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "enter ur api key"
}

data = {
  ##"text": "देवदत्त ओदनं पचति। देवदत्त ओदनं पचते। अथ प्रथमो ऽध्यायः राम एव लक्ष्मणस्य भ्राता",
  "text": "एषः उपन्यासः लीज़ेल मेमिन्गर नामकस्य बालिकायाः द्वितीयविश्वयुद्धस्य नाजी - जर्मनी - देशे तस्य अनुभवस्य कथां कथयति ।",
  "model_id": "eleven_multilingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output20.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
