import os
import json


# Funkcja do skanowania katalogu i wybierania plików .vtt bez "_translated"
def scan_vtt_files(base_path):
    sections = {}
    for root, dirs, files in os.walk(base_path):
        if "sekcja_nr_" in root:  # Sprawdzamy tylko katalogi sekcji
            section_name = os.path.basename(root)
            sections[section_name] = []
            for file in files:
                if file.endswith(".vtt") and "_translated" not in file:  # Filtrujemy pliki .vtt
                    file_path = os.path.join(root, file)
                    sections[section_name].append(file_path)
    return sections


# Funkcja do wczytywania zawartości plików .vtt
def read_vtt_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Błąd przy odczycie pliku {file_path}: {e}")
        return None


# Funkcja do tworzenia struktury JSON
def create_json_structure(sections):
    json_data = {}
    for section, files in sections.items():
        json_data[section] = {}
        for file_path in files:
            file_name = os.path.basename(file_path)
            print(f"Czytanie pliku: {file_name} w sekcji: {section}")
            content = read_vtt_content(file_path)
            if content:
                json_data[section][file_name] = {
                    "content": content
                }
    return json_data


# Funkcja do zapisu struktury JSON do pliku
def save_to_json(data, output_file=r"E:\XBLD_Adobe\course_vtt_data3.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Wyniki zapisano w pliku {output_file}")


# Główna funkcja
def main():
    # Ścieżka bazowa do folderu z kursami
    base_path = r"E:/KURS_POSPRODUKCJA"

    # Skanowanie struktury katalogów
    sections = scan_vtt_files(base_path)

    # Tworzenie struktury JSON
    json_data = create_json_structure(sections)

    # Zapisanie danych do pliku JSON
    save_to_json(json_data)


# Uruchomienie skryptu
if __name__ == "__main__":
    main()
