import openai
import webvtt

# Ustaw swój klucz OpenAI API
#api_key = "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"
api_key = ""
client = openai.OpenAI(api_key=api_key)  # Przekazanie klucza API

# Funkcja do ekstrakcji tekstu z pliku VTT
def extract_text_from_vtt(vtt_file):
    text = []
    for caption in webvtt.read(vtt_file):
        text.append(caption.text.strip())
    return " ".join(text)

# Funkcja do wysyłania zapytań do GPT-4
def summarize_with_gpt4(client, text_chunk):
    try:
        prompt = (
            "Summarize the most important information from the lecture below in English. "
            "Use precise terms and concepts related to GIS and Esri technologies, such as ArcGIS Online, File Geodatabases, "
            "and others. Focus on 2-3 key points using bullet points:\n\n"
            f"{text_chunk}"
        )
        response = client.chat.completions.create(
            model="gpt-4",  # Użycie modelu gpt-4
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
    except openai.OpenAIError as e:  # Obsługa błędów
        print(f"Error communicating with API: {e}")
        return "Failed to generate summary."

# Funkcja główna do analizy i generowania krótkiego streszczenia
def analyze_and_generate_summary(client, vtt_file, lecture_title):
    # Ekstrakcja tekstu z pliku VTT
    full_text = extract_text_from_vtt(vtt_file)
    print("Text extraction completed.")

    # Generowanie krótkiego streszczenia
    summary = summarize_with_gpt4(client, full_text)
    print("Summary generated.")

    # Formatowanie wyniku
    formatted_output = f"""
TN

Lecture: {lecture_title}

{summary}
"""
    return formatted_output.strip()

# Uruchomienie skryptu
if __name__ == "__main__":
    # Podaj ścieżkę do pliku VTT i tytuł wykładu
    vtt_file_path = r"C:\Users\bucha\Desktop\MODEL_AI\3 Dane do pobrania wykorzystywane podczas kursu_translated.vtt"
    lecture_title = "Creating templates"

    # Generowanie krótkiego streszczenia
    result = analyze_and_generate_summary(client, vtt_file_path, lecture_title)

    # Zapis wyniku do pliku tekstowego
    output_file_path = r"C:\Users\bucha\Desktop\MODEL_AI\short_summary_with_terms.txt"
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Short summary with precise GIS terms saved in file: {output_file_path}")
