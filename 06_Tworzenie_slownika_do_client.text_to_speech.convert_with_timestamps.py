import re

# Ścieżka do pliku
plik_VTT = r"E:\Kurs\TEST\10 Integracja z danymi GIS_translated.vtt"

# Funkcja do konwersji czasu na sekundy
def time_to_seconds(time_str):
    """Konwertuje czas w formacie HH:MM:SS.mmm na sekundy."""
    try:
        parts = time_str.split(':')
        h = int(parts[0])
        m = int(parts[1])
        s, ms = map(float, parts[2].split('.'))
        total_seconds = h * 3600 + m * 60 + s + ms / 1000
        return round(total_seconds, 2)
    except ValueError as e:
        raise ValueError(f"Invalid time format: {time_str}. Error: {e}")

# Funkcja do wczytywania segmentów z pliku VTT i tworzenia słownika movie_direct
def read_vtt_segments_to_movie_direct(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    segments = []
    current_segment = {}

    for line in lines:
        line = line.strip()
        if "-->" in line:
            timestamps = line.split("-->")
            start_time = time_to_seconds(timestamps[0].strip())
            end_time = time_to_seconds(timestamps[1].strip())
            current_segment['start'] = start_time
            current_segment['end'] = end_time
        elif line and 'start' in current_segment:
            current_segment['text'] = line
        elif not line and 'start' in current_segment and 'text' in current_segment:
            segments.append(current_segment)
            current_segment = {}
    if 'start' in current_segment and 'text' in current_segment:
        segments.append(current_segment)

    movie_direct = {
        'characters': [segment['text'] for segment in segments],
        'character_start_times_seconds': [segment['start'] for segment in segments],
        'character_end_times_seconds': [segment['end'] for segment in segments]
    }
    return movie_direct

# Wczytaj dane z pliku i utwórz słownik
movie_direct = read_vtt_segments_to_movie_direct(plik_VTT)

# Wyświetl wynik
print(movie_direct)
