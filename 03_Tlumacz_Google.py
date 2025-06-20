from googletrans import Translator

# Ścieżka do pliku VTT do przetłumaczenia
vtt_file_path = r'E:\Kurs\TEST\10 Integracja z danymi GIS.vtt'

# Ścieżka do zapisu przetłumaczonego pliku
translated_file_path = r'E:\Kurs\TEST\10 Integracja z danymi GIS_translated.vtt'

# Funkcja do tłumaczenia pliku VTT
def translate_vtt(file_path, translated_file_path, src_lang='pl', dest_lang='en'):
    try:
        # Wczytanie zawartości pliku VTT
        with open(file_path, 'r', encoding='utf-8') as file:
            vtt_content = file.read()

        # Inicjalizacja tłumacza
        translator = Translator()

        # Podział treści na linie
        vtt_lines = vtt_content.splitlines()

        # Przetwarzanie tłumaczenia, pomijanie sygnatur czasowych i nagłówków
        translated_lines = []
        for line in vtt_lines:
            if '-->' in line or line.strip() == '' or line.upper() == 'WEBVTT':
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

        # Scal przetłumaczone linie w nową zawartość VTT
        translated_vtt_content = '\n'.join(translated_lines)

        # Zapisz przetłumaczony plik
        with open(translated_file_path, 'w', encoding='utf-8') as translated_file:
            translated_file.write(translated_vtt_content)

        print(f"Przetłumaczony plik zapisano w: {translated_file_path}")

    except Exception as e:
        print(f"Wystąpił błąd podczas tłumaczenia pliku: {e}")

# Wywołanie funkcji
translate_vtt(vtt_file_path, translated_file_path)
