import os

# Ścieżka do katalogu z plikami
folder_path = r'C:\Users\bucha\Desktop\Streszczenie_9.6'
output_file = os.path.join(folder_path, 'Zespolony_plik.txt')

# Dokładne zakresy lekcji dla każdego rozdziału
chapter_ranges = {
    1: range(1, 8),
    2: range(8, 11),
    3: range(11, 24),
    4: range(24, 29),
    5: range(29, 36),
    6: range(36, 42),
    7: range(42, 65),
    8: range(65, 75),
    9: range(75, 78),
    10: range(78, 81),
    11: range(81, 84),
    12: range(84, 88),
    13: range(88, 96),
}

# Nazwy rozdziałów
chapter_names = {
    1: "Chapter Section 1 - Getting Started",
    2: "Chapter Section 2 - ArcGIS Experience Builder from Scratch",
    3: "Chapter Section 3 - ArcGIS Experience Builder from Scratch",
    4: "Chapter Section 4 - Map - Introduction",
    5: "Chapter Section 5 - Web Map Layer Grouping: Map Layers, Exclusive Visibility, Bookmarks",
    6: "Chapter Section 6 - Data Editing",
    7: "Chapter Section 7 - Data-Driven Widgets",
    8: "Chapter Section 8 - Map-Based Widgets",
    9: "Chapter Section 9 - 3D Elements - Widget Controller",
    10: "Chapter Section 10 - Dynamic Text - Data Views",
    11: "Chapter Section 11 - Templates",
    12: "Chapter Section 12 - ArcGIS Experience Builder (Developer Edition)",
    13: "Chapter Section 13 - Additional Content"
}

# Funkcja do pobrania numeru wykładu z nazwy pliku
def get_lecture_number(filename):
    try:
        return int(filename.split()[0])
    except ValueError:
        return None

# Sortowanie plików wg numeru wykładu
files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
sorted_files = sorted(files, key=lambda x: get_lecture_number(x) or 0)

# Tworzenie scalonego pliku
with open(output_file, 'w', encoding='utf-8') as outfile:
    current_chapter = None

    for file in sorted_files:
        lecture_number = get_lecture_number(file)

        if lecture_number:
            for chapter, lecture_range in chapter_ranges.items():
                if lecture_number in lecture_range:
                    chapter_name = chapter_names[chapter]
                    if chapter_name != current_chapter:
                        current_chapter = chapter_name
                        outfile.write(f"\n{current_chapter}\n\n")
                    break

        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='utf-8') as infile:
            content = infile.read()
            outfile.write(content + "\n\n")

print(f"Scalono pliki do: {output_file}")
