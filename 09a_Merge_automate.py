import os
from pydub import AudioSegment
import webvtt

def time_to_milliseconds(timestamp):
    """Konwersja czasu z formatu VTT na milisekundy."""
    hours, minutes, seconds = map(float, timestamp.split(':'))
    return int((hours * 3600 + minutes * 60 + seconds) * 1000)

def process_folder(folder_path):
    """Przetwarzanie jednego folderu w poszukiwaniu plików VTT i segmentów MP3."""
    folder_name = os.path.basename(folder_path)

    # Wyszukaj plik VTT zaczynający się od nazwy folderu
    vtt_files = [f for f in os.listdir(folder_path) if f.startswith(folder_name) and f.endswith(".vtt")]
    if not vtt_files:
        print(f"Brak pliku VTT w folderze: {folder_path}")
        return

    vtt_file = vtt_files[0]
    vtt_path = os.path.join(folder_path, vtt_file)

    # Znajdź wszystkie segmenty MP3 w folderze
    segments = sorted(
        [f for f in os.listdir(folder_path) if f.startswith("segment_nr_") and f.endswith(".mp3")],
        key=lambda x: int(x.split("_nr_")[1].split(".mp3")[0])
    )

    if not segments:
        print(f"Brak segmentów MP3 w folderze: {folder_path}")
        return

    print(f"Przetwarzanie pliku VTT: {vtt_file}")
    print(f"Znalezione segmenty: {segments}")

    # Wczytaj segmenty MP3
    segment_audios = [AudioSegment.from_file(os.path.join(folder_path, seg)) for seg in segments]

    combined_audio = AudioSegment.silent(duration=0)
    segment_index = 0

    # Przetwarzaj VTT i łącz segmenty
    for caption in webvtt.read(vtt_path):
        start_time = time_to_milliseconds(caption.start)
        end_time = time_to_milliseconds(caption.end)

        if len(combined_audio) < start_time:
            combined_audio += AudioSegment.silent(duration=start_time - len(combined_audio))

        if segment_index < len(segment_audios):
            combined_audio += segment_audios[segment_index]
            segment_index += 1

        if len(combined_audio) < end_time:
            combined_audio += AudioSegment.silent(duration=end_time - len(combined_audio))

    # Przygotowanie nazwy pliku wynikowego
    output_file_name = vtt_file.replace(".vtt", "_MP3_WYNIK.mp3")
    output_path = os.path.join(folder_path, output_file_name)

    # Eksport wynikowego pliku MP3
    combined_audio.export(output_path, format="mp3")
    print(f"Zapisano plik wynikowy: {output_path}")

def process_all_folders(root_folder):
    """Iteracja przez wszystkie foldery w podanej ścieżce i ich przetwarzanie."""
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            process_folder(folder_path)

# Ścieżka głównego folderu
root_folder = r"E:\\good_fr"
process_all_folders(root_folder)
