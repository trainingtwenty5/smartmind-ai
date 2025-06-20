import os
from elevenlabs import ElevenLabs
import json
from elevenlabs import Voice, VoiceSettings, play, save


# Funkcja do odczytu tekstu z pliku VTT
def read_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Filtrujemy tylko linie z tekstem (pomijając nagłówki i czasowe sygnatury)
    text_lines = [
        line.strip() for line in lines if '-->' not in line and line.strip() and not line.startswith("WEBVTT")
    ]
    return " ".join(text_lines)

# Ścieżka do pliku VTT
vtt_file_path = r"E:\XBLD_Adobe\KURS_POSPRODUKCJA\sekcja_nr_9\76 Skrzynka narzędziowa 3D – Widżet 3D Toolbox - kontroler lotu - Fly Controller_translated.vtt"

# Odczyt tekstu z pliku VTT
text = read_vtt_file(vtt_file_path)
print(text)


# Konfiguracja klienta ElevenLabs
client = ElevenLabs(api_key="sk_c09c6cca79cbb78942cbcb5946e2b7ccede077ed33b25340")

audio = client.generate(
    text=text,
    model="eleven_multilingual_v2",
    voice=Voice(
        voice_id='pwiYDAIKdosSgMYKMdqu',
        settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
    )
)
