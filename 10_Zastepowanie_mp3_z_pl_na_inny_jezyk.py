import ffmpeg
import os

def replace_audio_with_ffmpeg(video_path, audio_path, output_path):
    # Sprawdź, czy pliki istnieją
    if not os.path.exists(video_path):
        print(f"Błąd: Plik wideo {video_path} nie istnieje.")
        return
    if not os.path.exists(audio_path):
        print(f"Błąd: Plik audio {audio_path} nie istnieje.")
        return

    try:
        print("Rozpoczynanie procesu podmiany audio...")
        # Podmiana audio wideo za pomocą FFmpeg
        video_input = ffmpeg.input(video_path)
        audio_input = ffmpeg.input(audio_path)
        ffmpeg.output(video_input.video, audio_input.audio, output_path,
                      vcodec='copy', acodec='aac', strict='experimental').run()
        print(f"Sukces! Wynik zapisano w {output_path}")
    except ffmpeg.Error as e:
        print(f"Błąd podczas przetwarzania: {e.stderr.decode('utf8')}")

# Przykładowe użycie
if __name__ == "__main__":
    # Ścieżki do plików
    video_path = r"E:\KURS_POSPRODUKCJA_DONE\sekcja_nr_1\1\1 Edycja naszego pierwszego ArcGIS Experience Builder_en_p_1.mp4"
    audio_path = r"C:\Users\bucha\Desktop\A\1\1 Edycja naszego pierwszego ArcGIS Experience Builder_translated_translated_fr_MP3_WYNIK.mp3"
    output_path = r"C:\Users\bucha\Desktop\A\1\1 Edycja naszego pierwszego ArcGIS Experience Builder_fr_p_1_Skrypt.mp4"

    # Wywołanie funkcji
    replace_audio_with_ffmpeg(video_path, audio_path, output_path)
