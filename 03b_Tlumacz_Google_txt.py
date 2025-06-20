import os
from googletrans import Translator

# Funkcja do tłumaczenia pliku TXT
def translate_txt_file(file_path, src_lang='pl', dest_lang='en'):
    try:
        # Określenie ścieżki przetłumaczonego pliku
        dir_name, file_name = os.path.split(file_path)
        base_name, ext = os.path.splitext(file_name)
        translated_file_path = os.path.join(dir_name, f"{base_name}_translated{ext}")

        # Wczytanie zawartości pliku
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Inicjalizacja tłumacza
        translator = Translator()

        # Tłumaczenie zawartości linia po linii
        translated_lines = []
        for line in content:
            if line.strip() == '':
                translated_lines.append(line)  # Puste linie bez zmian
            else:
                try:
                    translated_text = translator.translate(line, src=src_lang, dest=dest_lang).text
                    translated_lines.append(translated_text + '\n')
                except Exception as e:
                    print(f"Błąd tłumaczenia linii: {line} - {e}")
                    translated_lines.append(line)

        # Zapisz przetłumaczony plik
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.writelines(translated_lines)

        print(f"Przetłumaczony plik zapisano: {translated_file_path}")

    except Exception as e:
        print(f"Wystąpił błąd z plikiem {file_path}: {e}")

# Funkcja do przetłumaczenia wszystkich plików TXT w katalogu
def translate_all_txt_files(directory, src_lang='pl', dest_lang='en'):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.txt'):  # Tylko pliki TXT
                file_path = os.path.join(root, file)
                print(f"Tłumaczenie pliku: {file_path}")
                translate_txt_file(file_path, src_lang, dest_lang)

# Podaj ścieżkę do folderu z plikami TXT
source_directory = r'C:\Users\bucha\Desktop\HTML'
translate_all_txt_files(source_directory)
