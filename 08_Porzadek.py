import os
import re

# Ścieżka do folderu
folder_path = r"E:\KURS_DONE\a"

# Funkcja do wyodrębnienia liczby z nazwy pliku
def extract_number(file_name):
    match = re.match(r"(\d+)", file_name)
    return int(match.group(1)) if match else float('inf')

# Sprawdzanie, czy folder istnieje
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Odczyt nazw plików w folderze
    files = os.listdir(folder_path)

    # Filtrowanie tylko plików (bez folderów)
    file_names = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    # Sortowanie plików według numerów na początku ich nazw
    sorted_files = sorted(file_names, key=extract_number)

    # Wyświetlenie posortowanych nazw plików
    print("Posortowane pliki w folderze:")
    for file_name in sorted_files:
        print(file_name)
else:
    print(f"Folder '{folder_path}' nie istnieje lub nie jest folderem.")
