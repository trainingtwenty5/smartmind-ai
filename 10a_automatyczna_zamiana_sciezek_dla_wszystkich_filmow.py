import ffmpeg
import os


def replace_audio_in_videos(base_video_folder, base_audio_folder, output_folder):
    # Przeszukaj katalog z filmami
    for file_name in os.listdir(base_video_folder):
        if file_name.endswith(".mp4"):
            video_path = os.path.join(base_video_folder, file_name)

            # Wyciągnij numer i nazwę z pliku wideo
            file_prefix = file_name.split(" ", 1)[0]  # Pierwszy fragment przed spacją (numer)
            audio_folder = os.path.join(base_audio_folder, file_prefix)

            if not os.path.exists(audio_folder):
                print(f"Folder {audio_folder} nie istnieje, pomijam.")
                continue

            # Znajdź odpowiadający plik audio
            audio_file_name = file_name.replace("_en_p_1.mp4", "_translated_translated_fr_MP3_WYNIK.mp3")
            audio_path = os.path.join(audio_folder, audio_file_name)

            if not os.path.exists(audio_path):
                print(f"Plik audio {audio_path} nie istnieje, pomijam.")
                continue

            # Tworzenie ścieżki do pliku wynikowego
            output_file_name = file_name.replace("_en_p_1.mp4", "_fr_p_1_Skrypt.mp4")
            output_path = os.path.join(output_folder, output_file_name)

            try:
                print(f"Podmieniam audio w pliku: {video_path}")
                # Podmiana audio wideo za pomocą FFmpeg
                video_input = ffmpeg.input(video_path)
                audio_input = ffmpeg.input(audio_path)
                ffmpeg.output(video_input.video, audio_input.audio, output_path,
                              vcodec='copy', acodec='aac', strict='experimental').run()
                print(f"Zakończono: {output_path}")
            except ffmpeg.Error as e:
                print(f"Błąd podczas przetwarzania pliku {video_path}: {e.stderr.decode('utf8')}")


# Przykładowe użycie
if __name__ == "__main__":
    # Ścieżki bazowe
    base_video_folder = r"E:\KURS_POSPRODUKCJA_DONE"
    base_audio_folder = r"E:\good_fr"
    output_folder = r"E:\good_fr"

    # Wywołanie funkcji
    replace_audio_in_videos(base_video_folder, base_audio_folder, output_folder)
