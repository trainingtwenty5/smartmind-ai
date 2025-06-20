import os
from pydub import AudioSegment
import webvtt

# Ścieżki do plików
input_folder = r"E:\good_fr\4"
vtt_file = "4 Opis danych wykorzystywanych podczas kursu_translated_translated_fr.vtt"
output_file = "4 Opis danych wykorzystywanych podczas kursu_translated_translated_fr_MP3_WYNIK2.mp3"

# Funkcja do konwersji czasu z VTT na milisekundy
def time_to_milliseconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.split(':'))
    return int((hours * 3600 + minutes * 60 + seconds) * 1000)

# Wczytanie pliku VTT i segmentów
combined_audio = AudioSegment.silent(duration=0)

# Automatyczne tworzenie listy segmentów
segments = sorted(
    [f for f in os.listdir(input_folder) if f.startswith("segment_nr_") and f.endswith(".mp3")],
    key=lambda x: int(x.split("_nr_")[1].split(".mp3")[0])
)

# Wyświetlenie listy segmentów
print("Znalezione segmenty:")
for seg in segments:
    print(seg)

segment_audios = [AudioSegment.from_file(os.path.join(input_folder, seg)) for seg in segments]

# Łączenie ścieżek na podstawie VTT
vtt_path = os.path.join(input_folder, vtt_file)
segment_index = 0  # Indeks segmentu MP3

for caption in webvtt.read(vtt_path):
    start_time = time_to_milliseconds(caption.start)
    end_time = time_to_milliseconds(caption.end)

    # Dodanie ciszy, jeśli potrzeba
    if len(combined_audio) < start_time:
        combined_audio += AudioSegment.silent(duration=start_time - len(combined_audio))

    # Dodanie segmentu audio
    if segment_index < len(segment_audios):
        combined_audio += segment_audios[segment_index]
        segment_index += 1

    # Dodanie ciszy po segmencie, jeśli to konieczne
    if len(combined_audio) < end_time:
        combined_audio += AudioSegment.silent(duration=end_time - len(combined_audio))

# Zapisanie wyniku
output_path = os.path.join(input_folder, output_file)
combined_audio.export(output_path, format="mp3")

print(f"Zapisano plik wynikowy: {output_path}")