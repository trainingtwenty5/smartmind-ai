import os
import time
import subprocess
import ffmpeg
from elevenlabs import ElevenLabs, save

# Funkcja do wyszukiwania pliku VTT w katalogu i podkatalogach
def find_vtt_file(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.vtt'):
                return os.path.join(root, file)
    return None

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
            if 'text' in current_segment:
                current_segment['text'] += " " + line
            else:
                current_segment['text'] = line
        elif not line and 'start' in current_segment and 'text' in current_segment:
            segments.append(current_segment)
            current_segment = {}
    if 'start' in current_segment and 'text' in current_segment:
        segments.append(current_segment)

    return segments

def create_silence_file(duration, output_file):
    """
    Tworzy plik MP3 z ciszą o podanym czasie trwania przy użyciu subprocess i FFmpeg.
    """
    try:
        command = [
            'ffmpeg',
            '-f', 'lavfi',                  # Format: filtr
            '-i', f'anullsrc=r=44100:cl=stereo',  # Źródło ciszy
            '-t', str(duration),            # Długość trwania ciszy
            '-q:a', '9',                    # Jakość audio
            output_file                     # Plik wyjściowy
        ]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Plik ciszy zapisany jako: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas generowania ciszy: {e.stderr.decode()}")

def time_to_seconds(timestamp):
    h, m, s = map(float, timestamp.split(':'))
    return h * 3600 + m * 60 + s

def merge_segments(segments, directory, output_file):
    inputs = []
    current_time = 0.0

    for idx, segment in enumerate(segments):
        mp3_file = os.path.join(directory, f"segment_nr_{idx}.mp3")
        if not os.path.exists(mp3_file):
            print(f"Plik {mp3_file} nie istnieje, pomijam...")
            continue

        segment_start = time_to_seconds(segment['start'])
        segment_end = time_to_seconds(segment['end'])

        if current_time < segment_start:
            silence_duration = segment_start - current_time
            silence_file = os.path.join(directory, f"silence_{idx}.mp3")
            create_silence_file(silence_duration, silence_file)
            inputs.append(ffmpeg.input(silence_file))
            current_time = segment_start

        inputs.append(ffmpeg.input(mp3_file))
        current_time = segment_end

    concat = ffmpeg.concat(*inputs, v=0, a=1)
    ffmpeg.output(concat, output_file).run(overwrite_output=True)
    print(f"Plik wynikowy zapisany jako {output_file}")

def main():
    directory = r"E:\\Kurs\\TEST"
    vtt_file = os.path.join(directory, "10 Integracja z danymi GIS_translated.vtt")
    if not os.path.exists(vtt_file):
        print("Plik VTT nie istnieje.")
        return

    segments = read_vtt_segments(vtt_file)
    print(f"Wczytano {len(segments)} segmentów.")
    print(segments)

    # Inicjalizacja klienta ElevenLabs
    client = ElevenLabs(api_key="sk_c09c6cca79cbb78942cbcb5946e2b7ccede077ed33b25340")

    # Generowanie plików MP3
    # for i, segment in enumerate(segments):
    #     if 'text' in segment:
    #         try:
    #             print(f"Generowanie głosu dla segmentu {i + 1}: {segment['text']}")
    #             audio = client.generate(
    #                 text=segment["text"],
    #                 voice="pwiYDAIKdosSgMYKMdqu",
    #                 model="eleven_multilingual_v2"
    #             )
    #             save(audio, os.path.join(directory, f'segment_nr_{i}.mp3'))
    #             print(f"Segment {i + 1} zapisany jako segment_nr_{i}.mp3")
    #             time.sleep(1)
    #         except Exception as e:
    #             print(f"Błąd podczas generowania segmentu {i + 1}: {e}")

    print("Wszystkie segmenty zostały wygenerowane.")

    # Łączenie plików MP3
    output_file = os.path.join(directory, "merged_output.mp3")
    merge_segments(segments, directory, output_file)

# Uruchomienie skryptu
if __name__ == "__main__":
    main()
