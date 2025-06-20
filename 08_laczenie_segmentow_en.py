import os
from pydub import AudioSegment
import webvtt

# Ścieżki do plików
input_folder = "E:/KURS_POSPRODUKCJA/sekcja_nr_3/13"
segments = [
    "segment_nr_0.mp3",
    "segment_nr_1.mp3",
    "segment_nr_2.mp3",
    "segment_nr_3.mp3",
    "segment_nr_4.mp3",
    "segment_nr_5.mp3",
    "segment_nr_6.mp3",
]
vtt_file = "13 Zarządzanie podstronami_translated.vtt"
output_file = "13 Zarządzanie podstronami_en_MP3_WYNIK2.mp3"

# Funkcja do konwersji czasu z VTT na milisekundy
def time_to_milliseconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.split(':'))
    return int((hours * 3600 + minutes * 60 + seconds) * 1000)

# Wczytanie pliku VTT i segmentów
combined_audio = AudioSegment.silent(duration=0)
silence = AudioSegment.silent(duration=1000)

segment_audios = [AudioSegment.from_file(os.path.join(input_folder, seg)) for seg in segments]

# Łączenie ścieżek na podstawie VTT
vtt_path = os.path.join(input_folder, vtt_file)
for caption in webvtt.read(vtt_path):
    start_time = time_to_milliseconds(caption.start)
    end_time = time_to_milliseconds(caption.end)
    segment_index = int(caption.text.strip())

    # Wstawienie ciszy przed segmentem, jeśli to konieczne
    if len(combined_audio) < start_time:
        combined_audio += AudioSegment.silent(duration=start_time - len(combined_audio))

    # Dodanie segmentu audio
    combined_audio += segment_audios[segment_index]

    # Dodanie ciszy po segmencie, jeśli to konieczne
    if len(combined_audio) < end_time:
        combined_audio += AudioSegment.silent(duration=end_time - len(combined_audio))

# Zapisanie wyniku
output_path = os.path.join(input_folder, output_file)
combined_audio.export(output_path, format="mp3")

print(f"Zapisano plik wynikowy: {output_path}")
