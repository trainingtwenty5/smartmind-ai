import os
import whisper
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# Funkcja do przetwarzania jednego pliku wideo
def process_video(input_video, srt_file, vtt_file, threshold=0.85):
    print(f"Processing file: {input_video}")

    # 1. Transcription using Whisper
    model = whisper.load_model("large")
    result = model.transcribe(input_video, language="en")  # Set language to English
    segments = result["segments"]
    nlp = spacy.load("en_core_web_sm")  # SpaCy for English language

    # 2. Duplicate analysis
    unique_segments = []
    seen_sentences = []
    removed_segments = []  # Collect removed segments

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
                    "reason": "duplicate"
                })
                break
        if not is_duplicate:
            unique_segments.append(segment)
        seen_sentences.append(text)

    # 3. Removing silence
    cleaned_segments = []
    for segment in unique_segments:
        start = segment["start"]
        end = segment["end"]
        duration = end - start
        if duration > 0.5:  # Keep only segments longer than 0.5s
            cleaned_segments.append(segment)

    # 4. Creating .srt and .vtt files
    # SRT file
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(cleaned_segments, start=1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"{i}\n")
            f.write(f"{format_timestamp_srt(start)} --> {format_timestamp_srt(end)}\n")
            f.write(f"{text}\n\n")
    print(f"SRT file saved: {srt_file}")

    # VTT file
    with open(vtt_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for segment in cleaned_segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"{format_timestamp_vtt(start)} --> {format_timestamp_vtt(end)}\n")
            f.write(f"{text}\n\n")
    print(f"VTT file saved: {vtt_file}")

# Function to format time in .srt style
def format_timestamp_srt(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Function to format time in .vtt style
def format_timestamp_vtt(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Function to traverse folders and subfolders
def process_videos_in_folder(input_folder):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".mp4"):
                input_video = os.path.join(root, filename)
                base_name = os.path.splitext(input_video)[0]
                srt_file = base_name + ".srt"
                vtt_file = base_name + ".vtt"
                process_video(input_video, srt_file, vtt_file)

# Main program
if __name__ == "__main__":
    input_folder = r"D:\XBLD_Adobe_2"  # Folder with input MP4 files

    process_videos_in_folder(input_folder)
    print("Processing of all files completed!")
