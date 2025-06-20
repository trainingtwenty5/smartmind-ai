import os
import whisper
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Funkcja do przetwarzania jednego pliku wideo
def process_video(input_video, srt_file, vtt_file, threshold=0.85):
    print(f"Przetwarzanie pliku: {input_video}")

    # 1. Transkrypcja za pomocą Whisper
    model = whisper.load_model("large")
    result = model.transcribe(input_video, language="pl")  # Ustawienie języka na polski
    segments = result["segments"]
    nlp = spacy.load("pl_core_news_sm")  # Spacy dla języka polskiego

    # 2. Analiza powtórzeń
    unique_segments = []
    seen_sentences = []
    removed_segments = []  # Zbieranie usuniętych segmentów

    for segment in segments:
        text = segment["text"]
        is_duplicate = False
        for seen_text in seen_sentences:
            similarity = cosine_similarity(
                [nlp(text).vector], [nlp(seen_text).vector]
            )[0][0]
            if similarity > threshold:
                is_duplicate = True
                removed_segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": text,
                    "reason": "powtórzenie"
                })
                break
        if not is_duplicate:
            unique_segments.append(segment)
        seen_sentences.append(text)

    # 3. Usuwanie ciszy
    cleaned_segments = []
    for segment in unique_segments:
        start = segment["start"]
        end = segment["end"]
        duration = end - start
        if duration > 0.5:  # Zachowaj tylko segmenty dłuższe niż 0.5s
            cleaned_segments.append(segment)

    # 4. Tworzenie plików .srt i .vtt
    # Plik .srt
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(cleaned_segments, start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"{i}\n")
            f.write(f"{format_timestamp_srt(start)} --> {format_timestamp_srt(end)}\n")
            f.write(f"{text}\n\n")
    print(f"Plik SRT zapisany: {srt_file}")

    # Plik .vtt
    with open(vtt_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for segment in cleaned_segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"{format_timestamp_vtt(start)} --> {format_timestamp_vtt(end)}\n")
            f.write(f"{text}\n\n")
    print(f"Plik VTT zapisany: {vtt_file}")

# Funkcja do formatowania czasu w stylu .srt
def format_timestamp_srt(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Funkcja do formatowania czasu w stylu .vtt
def format_timestamp_vtt(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Funkcja do przechodzenia przez foldery i podfoldery
def process_videos_in_folder(input_folder):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp4"):
                input_video = os.path.join(root, filename)
                base_name = os.path.splitext(input_video)[0]
                srt_file = base_name + ".srt"
                vtt_file = base_name + ".vtt"
                process_video(input_video, srt_file, vtt_file)

# Główna część programu
if __name__ == "__main__":
    input_folder = r"E:\fr_p_1"  # Folder z wejściowymi plikami MP4

    process_videos_in_folder(input_folder)
    print("Przetwarzanie wszystkich plików zakończone!")
