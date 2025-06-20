import os
import time
import subprocess
import elevenlabs
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play, save
import os
import ffmpeg
#
#
#
#
#
#
#
#

# Ścieżka do pliku
plik_VTT = r"C:\Users\bucha\Desktop\MODEL_AI_FR\1 Edycja naszego pierwszego ArcGIS Experience Builder_translated_translated_fr.vtt.vtt"
ffolder = 66
ssekcja = 'sekcja_nr_8'



# Funkcja do wczytywania segmentów z pliku VTT
def read_vtt_segments(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    segments = []
    current_segment = {}
    for line in lines:
        line = line.strip()
        if "-->" in line:
            timestamps = line.split("-->")
            current_segment['start'] = timestamps[0].strip()
            current_segment['end'] = timestamps[1].strip()
        elif line and 'start' in current_segment:
            current_segment['text'] = line
        elif not line and 'start' in current_segment and 'text' in current_segment:
            segments.append(current_segment)
            current_segment = {}
    if 'start' in current_segment and 'text' in current_segment:
        segments.append(current_segment)
        print(segments)
    return segments

segments = read_vtt_segments(plik_VTT)

#################################################### TWORZENIE SEKWENCJI GLOSOW ##########################################################################
#Inicjalizacja klienta ElevenLabs
client = ElevenLabs(
    api_key="sk_c09c6cca79cbb78942cbcb5946e2b7ccede077ed33b25340"
    #api_key="sk_b6d98b52161fc63568c6434e4c06c83fe9d6c5572dfef320",  # Defaults to ELEVEN_API_KEY # FISHFOUNDER
)




for i, segment in enumerate(segments):
    if 'text' in segment:
        try:


            print(segment["text"])
            # audio = client.generate(
            #     text=segment["text"],
            #     voice="pwiYDAIKdosSgMYKMdqu",
            #     model="eleven_multilingual_v2"
            # )

            audio = client.generate(
                text=segment["text"],
                model="eleven_multilingual_v2",
                voice=Voice(
                    voice_id='pwiYDAIKdosSgMYKMdqu',
                    settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
                )
            )

            save(audio, fr'E:\KURS_POSPRODUKCJA\{ssekcja}\{ffolder}\segment_nr_{i}.mp3')
            print(fr'segment_nr_{i} - zapisany')


            time.sleep(1)  # Krótka przerwa
        except Exception as e:
            print(f"Błąd podczas generowania dźwięku dla segmentu {i + 1}: {e}")

print("Wszystkie segmenty zostały wygenerowane.")

