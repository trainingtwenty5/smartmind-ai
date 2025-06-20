from transformers import pipeline
import os

# Ścieżka do folderu z plikami VTT
folder_path = r"C:\Users\bucha\Desktop\MODEL_AI"  # Zmień na właściwą ścieżkę

# Sprawdzenie dostępności PyTorch
try:
    import torch
except ImportError:
    raise ImportError("PyTorch nie jest zainstalowany. Zainstaluj PyTorch, aby kontynuować.")

# Inicjalizacja modelu do streszczania tekstu
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

# Iteracja po plikach VTT w folderze
for filename in os.listdir(folder_path):
    if filename.endswith(".vtt"):
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                vtt_content = f.read()

            # Usunięcie znaczników VTT i pozostawienie tylko tekstu
            text = "".join([line for line in vtt_content.splitlines() if not line.startswith("WEBVTT") and not line.startswith("00:") and not line.strip() == ""])

            # Wygenerowanie streszczenia
            summary = summarizer(text, max_length=1330, min_length=330, do_sample=False)

            # Zapis streszczenia do pliku tekstowego
            summary_filename = filename[:-4] + "_summary.txt"
            summary_filepath = os.path.join(folder_path, summary_filename)
            with open(summary_filepath, "w", encoding="utf-8") as summary_file:
                summary_file.write(summary[0]["summary_text"])
            print(f"Streszczenie dla pliku {filename} zostało zapisane do {summary_filename}")

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {filename}: {e}")
