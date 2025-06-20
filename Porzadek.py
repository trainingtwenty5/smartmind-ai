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

# Funkcja do podziału tekstu na fragmenty
def split_text(text, max_tokens=300):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

# Iteracja po plikach VTT w folderze
for filename in os.listdir(folder_path):
    if filename.endswith(".vtt"):
        filepath = os.path.join(folder_path, filename)
        try:
            print(f"\nPrzetwarzanie pliku: {filename}")

            # Czy plik istnieje i ma zawartość
            if not os.path.isfile(filepath) or os.path.getsize(filepath) == 0:
                print(f"Plik {filename} jest pusty lub nie istnieje.")
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                vtt_content = f.read()

            # Usunięcie znaczników VTT i pozostawienie tylko tekstu
            text = "".join([line for line in vtt_content.splitlines()
                            if not line.startswith("WEBVTT")
                            and not line.startswith("00:")
                            and not line.strip() == ""])

            # Czy tekst po przetworzeniu jest pusty
            if not text.strip():
                print(f"Tekst w pliku {filename} jest pusty po usunięciu znaczników.")
                continue


            print(f"Długość tekstu po przetworzeniu: {len(text)} znaków.")

            # Podział tekstu na mniejsze fragmenty i generowanie streszczeń
            summaries = []
            for chunk in split_text(text, max_tokens=300):  # Zmniejszono wielkość fragmentów
                try:
                    # Dostosowanie max_length i min_length do długości fragmentu
                    max_length = min(1330, len(chunk.split()) // 2)
                    min_length = min(330, len(chunk.split()) // 4)
                    summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                    summaries.append(summary[0]["summary_text"])
                except Exception as chunk_error:
                    print(f"Błąd podczas przetwarzania fragmentu pliku {filename}: {chunk_error}")

            # Sprawdzenie, czy wygenerowano jakiekolwiek streszczenia
            if not summaries:
                print(f"Nie udało się wygenerować streszczenia dla pliku {filename}.")
                continue

            # Połączenie streszczeń w całość
            final_summary = " ".join(summaries)

            # Zapisanie streszczenia do pliku tekstowego
            summary_filename = filename[:-4] + "_summary.txt"
            summary_filepath = os.path.join(folder_path, summary_filename)
            with open(summary_filepath, "w", encoding="utf-8") as summary_file:
                summary_file.write(final_summary)
            print(f"Streszczenie dla pliku {filename} zostało zapisane do {summary_filename}")

        except Exception as e:
            print(f"Błąd podczas przetwarzania pliku {filename}: {e}")
