import os
import re
import openai
import webvtt

# Ustaw swój klucz OpenAI API
api_key = "XXX"
#api_key = ""


client = openai.OpenAI(api_key=api_key)  # Przekazanie klucza API

# Funkcja do ekstrakcji tekstu z pliku VTT
def extract_text_from_vtt(vtt_file):
    text = []
    for caption in webvtt.read(vtt_file):
        text.append(caption.text.strip())
    return " ".join(text)

# Funkcja do przetwarzania nazwy pliku
def process_file_name(file_name):
    # Usunięcie numeru, "_translated" oraz ".vtt"
    cleaned_name = re.sub(r"^\d+\s", "", file_name)  # Usuwa numer na początku
    cleaned_name = cleaned_name.replace("_translated", "").replace(".vtt", "")
    return cleaned_name

# Funkcja do tłumaczenia tytułu na angielski
def translate_title(client, title):
    try:
        prompt = f"Translate the following title from Polish to English:\n\n{title}"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant specializing in translations from Polish to English."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"Error translating title: {e}")
        return "Translation failed"

# Funkcja do wysyłania zapytań do GPT-4 w celu stworzenia streszczenia
def summarize_with_gpt4(client, text_chunk):
    try:
        prompt = (
            "Summarize the most important information from the lecture below in English. "
            "Use precise terms and concepts related to GIS and Esri technologies, such as ArcGIS Online, File Geodatabases, "
            "and others. Focus on 2-3 key points using bullet points:\n\n"
            f"{text_chunk}"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You are an AI assistant with expertise in GIS and Esri technologies. "
                    "You use precise terminology and concepts, ensuring technical accuracy when summarizing lectures. "
                    "Common terms include ArcGIS Online, File Geodatabases, hosted feature layers, and other GIS-specific vocabulary."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"Error communicating with API: {e}")
        return "Failed to generate summary."

# Funkcja główna do analizy i generowania streszczenia dla wszystkich plików w folderze
def process_all_vtt_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".vtt"):
            input_file_path = os.path.join(folder_path, file_name)

            # Przetwarzanie nazwy pliku na tytuł wykładu
            original_title = process_file_name(file_name)
            translated_title = translate_title(client, original_title)

            # Generowanie nazwy pliku wynikowego
            output_file_name = os.path.splitext(file_name)[0] + "_summary_esri.txt"
            output_file_path = os.path.join(folder_path, output_file_name)

            # Ekstrakcja tekstu z pliku
            full_text = extract_text_from_vtt(input_file_path)
            print(f"Processing file: {file_name}")

            # Generowanie streszczenia
            summary = summarize_with_gpt4(client, full_text)

            # Formatowanie wyniku
            formatted_output = f"""
TN

Lecture: {translated_title}

{summary}
""".strip()

            # Zapis streszczenia do pliku
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(formatted_output)
            print(f"Summary saved: {output_file_name}")

# Uruchomienie skryptu
if __name__ == "__main__":
    # Podaj ścieżkę do folderu z plikami VTT
    folder_path = r"C:\Users\bucha\Desktop\MODEL_AI"

    # Przetwarzanie wszystkich plików VTT
    process_all_vtt_files(folder_path)

    print("All summaries have been generated and saved.")
