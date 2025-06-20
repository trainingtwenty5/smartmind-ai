import elevenlabs
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_c09c6cca79cbb78942cbcb5946e2b7ccede077ed33b25340", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="Bonjour! Ciao! Cześć!",
  voice="pwiYDAIKdosSgMYKMdqu",
  model="eleven_multilingual_v2"
)

play(audio)
save(audio,r'C:\Users\bucha\Downloads\glos\test.mp3')