import os
import re
import openai
import webvtt

# Ustaw swój klucz OpenAI API
api_key = "XXX"
client = openai.OpenAI(api_key=api_key)  # Przekazanie klucza API

# Funkcja do ekstrakcji tekstu z pliku VTT
def extract_text_from_vtt(vtt_file):
    text = []
    for caption in webvtt.read(vtt_file):
        text.append(caption.text.strip())
    return " ".join(text)

# Funkcja do generowania pytań i ćwiczenia
def generate_questions_and_task(client, text):
    try:
        prompt = (
            "Based on the following lecture transcript, generate two multiple-choice questions (each with options a, b, c), "
            "where the correct answer is explained and incorrect answers are justified. Also, create one exercise that the viewer "
            "could do after watching the video. Provide the output in Polish and English, formatted as follows:\n\n"
            "QUESTION 1:\nQUESTION 2:\nTASK 1:\n"
            f"\n\nTranscript:\n{text}"
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI specialized in educational content generation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
        print(f"Error generating questions and tasks: {e}")
        return "Failed to generate questions and tasks."

# Funkcja główna do analizy i generowania pytań i ćwiczenia dla wszystkich plików w folderze
def process_all_vtt_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".vtt"):
            input_file_path = os.path.join(folder_path, file_name)

            # Przetwarzanie nazwy pliku na tytuł wykładu
            original_title = re.sub(r"^\d+\s", "", file_name.replace("_translated", "").replace(".vtt", ""))

            # Generowanie nazwy pliku wynikowego
            output_file_name = os.path.splitext(file_name)[0] + "_questions_and_task.txt"
            output_file_path = os.path.join(folder_path, output_file_name)

            # Ekstrakcja tekstu z pliku
            full_text = extract_text_from_vtt(input_file_path)
            print(f"Processing file: {file_name}")

            # Generowanie pytań i ćwiczenia
            questions_and_task = generate_questions_and_task(client, full_text)

            # Zapis pytań i ćwiczenia do pliku
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(f"Lecture: {original_title}\n\n{questions_and_task}")
            print(f"Questions and task saved: {output_file_name}")

# Uruchomienie skryptu
if __name__ == "__main__":
    # Podaj ścieżkę do folderu z plikami VTT
    folder_path = r"C:\\Users\\bucha\\Desktop\\MODEL_AI"

    # Przetwarzanie wszystkich plików VTT
    process_all_vtt_files(folder_path)

    print("All questions and tasks have been generated and saved.")