import os
import ffmpeg

def get_video_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Błąd podczas pobierania czasu trwania dla pliku {file_path}: {e}")
        return 0

if __name__ == "__main__":
    input_folder = r"E:\KURS_DONE\a"  # Folder wejściowy
    total_duration = 0

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp4"):  # Przetwarzaj tylko pliki MP4
                file_path = os.path.join(root, filename)
                duration = get_video_duration(file_path)
                total_duration += duration
                print(f"Plik: {filename}, Czas trwania: {duration / 60:.2f} minut")

    total_duration_minutes = total_duration / 60
    print(f"\nCałkowity czas trwania plików MP4: {total_duration:.2f} sekund ({total_duration_minutes:.2f} minut)")