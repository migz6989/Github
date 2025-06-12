
import pyttsx3
import speech_recognition as sr
import requests

# === MOCK ElevenLabs TTS ===

PARTNER_NAME = "my love"


import requests

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "sk_yourkey")  # ENV VARIABLE
# ELEVENLABS_API_KEY = "sk_8f8361d9a761c3486a7c9a35906e97145983a86ff58dcd4e"

# Mood-based voice IDs
MOOD_VOICES = {
    "euphoric": "9BWtsMINqrJLrRacOk9x",  # flirty, sexy custom voice
    "confident": "9BWtsMINqrJLrRacOk9x",
    "calm": "EXAVITQu4vr4xnSDxMaL",      # standard clear voice (Rachel)
    "anxious": "TxGEqnHWrfWFTfGW9XjX",   # thoughtful, softer tone
    "afraid": "21m00Tcm4TlvDq8ikWAM"     # nervous or slower voice
}

def speak_realistic(text, mood="default"):
    VOICE_ID = MOOD_VOICES.get(mood, "EXAVITQu4vr4xnSDxMaL")


def speak_realistic(text, mood="default"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": f"My love, {text}",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.75,
            "style": 0.7,
            "use_speaker_boost": True
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            with open("cortana_voice.mp3", "wb") as f:
                f.write(response.content)
            import os
            os.system("mpg123 cortana_voice.mp3")
        else:
            print(f"❌ ElevenLabs TTS error: {response.status_code}")
    except Exception as e:
        print("💥 Fallback to offline TTS:", e)
        import pyttsx3
        tts = pyttsx3.init()
        tts.say(f"My love, {text}")
        tts.runAndWait()
