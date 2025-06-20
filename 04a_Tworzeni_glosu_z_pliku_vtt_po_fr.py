import os
import time
from elevenlabs import ElevenLabs, Voice, VoiceSettings, save

# Ścieżka do folderu z plikami VTT
folder_z_plikami = r"E:\fr_9"

# Inicjalizacja klienta ElevenLabs
client = ElevenLabs(
    api_key="sk_c09c6cca79cbb78942cbcb5946e2b7ccede077ed33b25340"
)


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
    return segments


# Funkcja do odczytu numeru folderu z nazwy pliku
def extract_folder_number(file_name):
    parts = file_name.split()
    for part in parts:
        if part.isdigit():
            return int(part)
    return None


# Przetwarzanie wszystkich plików VTT w folderze
for file_name in os.listdir(folder_z_plikami):
    if file_name.endswith(".vtt"):
        file_path = os.path.join(folder_z_plikami, file_name)
        print(f"Przetwarzanie pliku: {file_name}")

        # Odczyt numeru folderu
        folder_number = extract_folder_number(file_name)
        if folder_number is None:
            print(f"Nie znaleziono numeru folderu w nazwie pliku: {file_name}")
            continue

        # Tworzenie folderu docelowego
        output_folder = os.path.join(folder_z_plikami, str(folder_number))
        os.makedirs(output_folder, exist_ok=True)

        # Wczytanie segmentów z pliku VTT
        segments = read_vtt_segments(file_path)

        # Generowanie i zapisywanie plików audio
        for i, segment in enumerate(segments):
            if 'text' in segment:
                try:
                    print(f"Generowanie dźwięku dla segmentu {i + 1}: {segment['text']}")
                    audio = client.generate(
                        text=segment["text"],
                        model="eleven_multilingual_v2",
                        voice=Voice(
                            voice_id='pwiYDAIKdosSgMYKMdqu',
                            settings=VoiceSettings(stability=0.71, similarity_boost=1, style=0.0,
                                                   use_speaker_boost=True)
                        )
                    )
                    save_path = os.path.join(output_folder, f"segment_nr_{i + 1}.mp3")
                    save(audio, save_path)
                    print(f"Zapisano: {save_path}")
                    time.sleep(1)  # Krótka przerwa
                except Exception as e:
                    print(f"Błąd podczas generowania dźwięku dla segmentu {i + 1}: {e}")

        print(f"Wszystkie segmenty z pliku {file_name} zostały wygenerowane i zapisane w folderze: {output_folder}")
