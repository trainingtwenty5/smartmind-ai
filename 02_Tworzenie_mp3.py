import os
import ffmpeg
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def extract_audio_ffmpeg_python(input_video, output_audio):
    print(f"Wyciąganie audio z pliku: {input_video}")
    try:
        (
            ffmpeg
            .input(input_video)        # Wczytaj plik wejściowy
            .output(output_audio, qscale=0, map='a')  # Wyjście audio w wysokiej jakości
            .run(overwrite_output=True)  # Uruchomienie FFmpeg
        )
        print(f"Audio zapisane w: {output_audio}")
    except ffmpeg.Error as e:
        print(f"Błąd podczas wyciągania audio: {e}")

# Główna część programu
if __name__ == "__main__":
    input_folder = r"E:\KURS_POSPRODUKCJA\sekcja_nr_3_en"  # Folder z wejściowymi plikami MP4

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp4"):  # Przetwarzaj tylko pliki MP4
                input_video = os.path.join(root, filename)
                output_audio = os.path.splitext(input_video)[0] + ".mp3"  # Plik wyjściowy MP3
                extract_audio_ffmpeg_python(input_video, output_audio)
