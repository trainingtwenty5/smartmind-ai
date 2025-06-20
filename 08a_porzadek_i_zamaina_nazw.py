import os
import re

# Ścieżka do folderu
folder_path = r"E:\KURS_DONE\a"

# Lista nowych nazw plików w poprawnej kolejności
new_names = [
    "Lecture: Editing our first ArcGIS Experience Builder",
    "Lecture: Data to download used during the course",
    "Lecture: Description of the data used during the course",
    "Lecture: Lecture: Web Map Configuration",
    "Lecture: Interface Service and Application Theme",
    "Lecture: Integration with GIS data",
    "Lecture: Managing Pages",
    "Lecture: Managing Subpages",
    "Lecture: Window Management",
    "Lecture: Modifying the position of widgets",
    "Lecture: Column Layout, Rows, Fixed Panel",
    "Lecture: Sidebar Layout",
    "Lecture: Grid System",
    "Lecture: Section Layout",
    "Lecture: Section Layout -complement- changing the name of the section and the order of views",
    "Lecture: Layout",
    "Lecture: Accordion arrangement",
    "Lecture: Size - Position",
    "Lecture: Map",
    "Lecture: Map - Complement - Trigger",
    "Lecture: Map - complement - relations - A11Y",
    "Lecture: A11Y - supplement",
    "Lecture: Map Layers",
    "Lecture: Map layers - managing visibility using groups",
    "Lecture: Many map layer widgets with customized access to layers",
    "Lecture: Bookmark - as a tool for grouping layers",
    "Lecture: Map Layers - Exclusive Visibility",
    "Lecture: Creating a new layer in ArcGIS Online",
    "Lecture: Editing",
    "Lecture: Attribute Editing - Table",
    "Lecture: Editing Attributes - Map",
    "Lecture: Elevation profile",
    "Lecture: Publishing data from ArcGIS Pro - Timeline",
    "Lecture: Timeline",
    "Lecture: List",
    "Lecture: List - Trigger - Actions",
    "Lecture: Filter - Filter",
    "Lecture: Filter - New Group",
    "Lecture: Filter - Custom Filter",
    "Lecture: Card",
    "Lecture: Query",
    "Lecture: Search",
    "Lecture: Search - Search - Trigger",
    "Lecture: Add Data",
    "Lecture: Choose - Select - Introduction to Framework",
    "Lecture: Select",
    "Lecture: Interactivity of the application - URL",
    "Lecture: Configuration with Dashboard - URL",
    "Lecture: Survey - Survey123",
    "Lecture: Survey - Survey123 - GlobalID",
    "Lecture: Report - Feature Report - Survey123",
    "Lecture: Chart",
    "Lecture: Chart - Chart - Dashboard",
    "Lecture: Chart - Chart - Framework",
    "Lecture: Rolling - Swipe",
    "Lecture: Rolling - Swipe - Tabs - Bookmarks",
    "Lecture: Near Me",
    "Lecture: My Location",
    "Lecture: Modeling Program - Suitability Modeler and Business Analyst - Utility Services",
    "Lecture: Directions and Print",
    "Lecture: Analysis",
    "Lecture: Analysis - Continued",
    "Lecture: Measurement - Coordinates - Coordinate Conversion",
    "Lecture: 3D Toolbox - 3D Widget Toolbox - Flight Controller - Fly Controller",
    "Lecture: Widget Controller",
    "Lecture: Expressions - Dynamic Text",
    "Lecture: Views",
    "Lecture: Creating templates",
    "Lecture: Generally about templates - Full screen - Grid - Scrollable",
    "Lecture: How to Deploy Customized Widgets of XBLD on ArcGIS Online Using AWS",
    "Lecture: Install XBLD Locally and Use it in ArcGIS Online - Server - Client",
    "Lecture: How to Deploy Customized Widgets of XBLD on ArcGIS Online - Locally",
    "Lecture: Interface - Express Mode",
    "Lecture: Disconnecting Views - Application Responsiveness - Full Screen - Tablet - Phone",
    "Lecture: Copying widgets between pages",
    "Lecture: Data Update - Truncate - Append",
    "Lecture: general – Survey123"
]

# Funkcja do wyodrębnienia liczby z nazwy pliku
def extract_number(file_name):
    match = re.match(r"(\d+)", file_name)
    return int(match.group(1)) if match else float('inf')

# Funkcja do usuwania niedozwolonych znaków z nazw plików
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Sprawdzanie, czy folder istnieje
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Odczyt nazw plików w folderze
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sortowanie plików według numeracji
    sorted_files = sorted(files, key=extract_number)

    # Sprawdzanie, czy liczba plików odpowiada liczbie nowych nazw
    if len(sorted_files) != len(new_names):
        print(f"Błąd: Liczba plików ({len(sorted_files)}) nie odpowiada liczbie nowych nazw ({len(new_names)}).")
    else:
        # Przechodzenie przez pliki i zmiana ich nazw
        for old_name, new_name in zip(sorted_files, new_names):
            # Dodanie rozszerzenia z oryginalnego pliku
            extension = os.path.splitext(old_name)[1]
            sanitized_new_name = sanitize_filename(new_name) + extension
            old_file_path = os.path.join(folder_path, old_name)
            new_file_path = os.path.join(folder_path, sanitized_new_name)

            # Zmiana nazwy pliku
            os.rename(old_file_path, new_file_path)
            print(f"Zmieniono nazwę: '{old_name}' -> '{sanitized_new_name}'")
else:
    print(f"Folder '{folder_path}' nie istnieje lub nie jest folderem.")
