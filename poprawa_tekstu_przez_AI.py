import os
import re
import openai
import webvtt

# Ustaw swój klucz OpenAI API
client = openai.OpenAI(api_key=api_key)  # Przekazanie klucza API


# Funkcja do ekstrakcji tekstu z pliku VTT
def extract_text_from_vtt(vtt_file):
    """Ekstrakcja tekstu z pliku VTT"""
    text = []
    for caption in webvtt.read(vtt_file):
        text.append(caption.text.strip())
    return " ".join(text)


def correct_transcription_with_ai(client, text):
    """Poprawianie błędów w transkrypcji za pomocą AI"""
    prompt = (
        "Correct any errors in terminology, spelling, and grammar in the following text, "
        "ensuring proper terminology related to ArcGIS and replacing abbreviations with full forms. "
        "Fix any repeated words and incorrect names of locations. Output only the corrected text.\n\n"
        f"Text:\n{text}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are an AI specialized in text correction and transcription refinement."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"Error correcting transcription: {e}")
        return text


def process_all_vtt_files(folder_path):
    """Przetwarzanie wszystkich plików VTT w folderze"""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".vtt"):
            input_file_path = os.path.join(folder_path, file_name)
            output_file_name = os.path.splitext(file_name)[0] + "_checked.txt"
            output_file_path = os.path.join(folder_path, output_file_name)

            # Ekstrakcja i poprawa tekstu
            full_text = extract_text_from_vtt(input_file_path)
            corrected_text = correct_transcription_with_ai(client, full_text)

            # Zapis poprawionego tekstu
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(corrected_text)

            print(f"Poprawiona transkrypcja zapisana: {output_file_name}")


if __name__ == "__main__":
    folder_path = r"C:\\Users\\bucha\\Desktop\\MODEL_AI"
    process_all_vtt_files(folder_path)
    print("Wszystkie pliki zostały poprawione i zapisane.")
