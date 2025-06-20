import os
from googletrans import Translator

# Funkcja do tłumaczenia plików VTT i SRT
def translate_file(file_path, src_lang='en', dest_lang='fr'):
    try:
        # Określenie ścieżki zapisu przetłumaczonego pliku
        dir_name, file_name = os.path.split(file_path)
        base_name, ext = os.path.splitext(file_name)
        translated_file_path = os.path.join(dir_name, f"{base_name}_translated_fr{ext}")

        # Wczytanie zawartości pliku
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Inicjalizacja tłumacza
        translator = Translator()

        # Przetwarzanie zawartości w zależności od rozszerzenia pliku
        lines = content.splitlines()
        translated_lines = []
        for line in lines:
            if '-->' in line or line.strip() == '' or line.upper() in ['WEBVTT', '']:
                # Kopiowanie sygnatur czasowych i nagłówków bez zmian
                translated_lines.append(line)
            else:
                # Tłumaczenie treści
                try:
                    translated_text = translator.translate(line, src=src_lang, dest=dest_lang).text
                    translated_lines.append(translated_text)
                except Exception as e:
                    print(f"Błąd tłumaczenia linii: {line} - {e}")
                    translated_lines.append(line)  # Zapisz oryginalny tekst w przypadku błędu

        # Formatowanie pliku SRT, jeśli to konieczne
        if ext.lower() == '.srt':
            translated_lines = correct_srt_format(translated_lines)

        # Scal przetłumaczone linie w nową zawartość
        translated_content = '\n'.join(translated_lines)

        # Zapisz przetłumaczony plik
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_content)

        print(f"Przetłumaczony plik zapisano w: {translated_file_path}")

    except Exception as e:
        print(f"Wystąpił błąd podczas tłumaczenia pliku: {file_path} - {e}")

# Funkcja do poprawiania formatowania SRT
def correct_srt_format(lines):
    corrected_lines = []
    for line in lines:
        if '-->' in line or line.strip() == '':
            corrected_lines.append(line)
        else:
            corrected_lines.append(line)
    return corrected_lines

# Funkcja do przeszukiwania katalogów i tłumaczenia plików
def translate_files_in_directory(directory, src_lang='en', dest_lang='fr'):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.vtt', '.srt')):
                file_path = os.path.join(root, file)
                print(f"Tłumaczenie pliku: {file_path}")
                translate_file(file_path, src_lang, dest_lang)

# Przykład użycia
# Podaj ścieżkę do katalogu, który chcesz przeszukać
source_directory = r'E:\fr_9'
translate_files_in_directory(source_directory)
