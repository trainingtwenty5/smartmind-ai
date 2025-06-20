import os

# Ścieżka do folderu
folder_path = r"E:\KURS_DONE\a"

# Mapowanie nowych nazw na stare
file_mapping = {
    'Lecture Editing our first ArcGIS Experience Builder.mp4': '1 Edycja naszego pierwszego ArcGIS Experience Builder_en_2.mp4',
    'Lecture Data to download used during the course.mp4': '10 Integracja z danymi GIS_en_2.mp4',
    'Lecture Description of the data used during the course.mp4': '12 Zarządzanie stronami (w)_en_2.mp4',
    'Lecture Lecture Web Map Configuration.mp4': '13 Zarządzanie podstronami_en_2.mp4',
    'Lecture Interface Service and Application Theme.mp4': '14 Zarządzanie oknami_en_2.mp4',
    'Lecture Integration with GIS data.mp4': '15 Modyfikowanie położenia widżetów (w)_en_2.mp4',
    'Lecture Managing Pages.mp4': '16 Układ Kolumny, Wiersze, Stały Panel (w)_en_2.mp4',
    'Lecture Managing Subpages.mp4': '17 Układ Pasek boczny_en_2.mp4',
    'Lecture Window Management.mp4': '18 Układ Siatka_en_2.mp4',
    'Lecture Modifying the position of widgets.mp4': '19 Układ Sekcje_en_2.mp4',
    'Lecture Column Layout, Rows, Fixed Panel.mp4': '20 Układ Sekcje -dopełnienie- zmiana nazwy sekcji oraz kolejności widoków_en_2.mp4',
    'Lecture Sidebar Layout.mp4': '21 Układ Przycisk (w)_en_2.mp4',
    'Lecture Grid System.mp4': '22 Układ akordeonowy_en_2.mp4',
    'Lecture Section Layout.mp4': '23 Rozmiar - Pozycja_en_2.mp4',
    'Lecture Section Layout -complement- changing the name of the section and the order of views.mp4': '24 Mapa (w)_en_2.mp4',
    'Lecture Layout.mp4': '25 Mapa - dopełnienie - Trigger_en_2.mp4',
    'Lecture Accordion arrangement.mp4': '26 Mapa - dopełnienie - relacje - A11Y_en_2.mp4',
    'Lecture Size - Position.mp4': '27 A11Y - dopelnienie ‐ Wykonano za pomocą Clipchamp_en_2.mp4',
    'Lecture Map.mp4': '3 Dane do pobrania wykorzystywane podczas kursu_en_2.mp4',
    'Lecture Map - Complement - Trigger.mp4': '30 Warstwy mapy_en_2.mp4',
    'Lecture Map - complement - relations - A11Y.mp4': '31 Warstwy mapy - zarządzanie widocznością za pomocą grup_1_en_2.mp4',
    'Lecture A11Y - supplement.mp4': '32 Wiele widżetów warstw mapy z dostosowanym dostępem do warstw_en_2.mp4',
    'Lecture Map Layers.mp4': '33 Zakładka - jako narzędzie do grupowania warstw_en_2.mp4',
    'Lecture Map layers - managing visibility using groups.mp4': '34 Warstwy mapy - Ekskluzywny widoczności_en_2.mp4',
    'Lecture Many map layer widgets with customized access to layers.mp4': '37 Tworzenie nowej warstwy w ArcGIS Online_en_2.mp4',
    'Lecture Bookmark - as a tool for grouping layers.mp4': '38 Edycja - Edit_en_2.mp4',
    'Lecture Map Layers - Exclusive Visibility.mp4': '39 Edycja atrybutów - Tabela_en_2.mp4',
    'Lecture Creating a new layer in ArcGIS Online.mp4': '4 Opis danych wykorzystywanych podczas kursu_en_2.mp4',
    'Lecture Editing.mp4': '40 Edycja atrybutów - Mapa_en_2.mp4',
    'Lecture Attribute Editing - Table.mp4': '41 Profil wysokościowy_en_2.mp4',
    'Lecture Editing Attributes - Map.mp4': '43 Publikowanie danych z ArcGIS Pro – Oś czasu_en_2.mp4',
    'Lecture Elevation profile.mp4': '44 Oś czasu - Timeline_en_2.mp4',
    'Lecture Publishing data from ArcGIS Pro - Timeline.mp4': '45 Lista - List_en_2.mp4',
    'Lecture Timeline.mp4': '46 Lista - Trigger - Akcje_en_2.mp4',
    'Lecture List.mp4': '47 Filtr - Filter_en_2.mp4',
    'Lecture List - Trigger - Actions.mp4': '48 Filtr - Nowa grupa - Filter - New group_en_2.mp4',
    'Lecture Filter - Filter.mp4': '49 Filtr - Nowy niestandardowy - Filter - custom filter_en_2.mp4',
    'Lecture Filter - New Group.mp4': '5 Konfiguracja Web Mapy_en_2.mp4',
    'Lecture Filter - Custom Filter.mp4': '50 Karta - Card_en_2.mp4',
    'Lecture Card.mp4': '51 Zapytanie - Query_en_2.mp4',
    'Lecture Query.mp4': '52 Szukaj - Search_en_2.mp4',
    'Lecture Search.mp4': '53 Szukaj - Search - Trigger_en_2.mp4',
    'Lecture Search - Search - Trigger.mp4': '54  Dodaj dane - Add Data_en_2.mp4',
    'Lecture Add Data.mp4': '56 Wybierz - Select - Wprwoadzenie do Framework_en_2.mp4',
    'Lecture Choose - Select - Introduction to Framework.mp4': '57 Wybierz - Select_en_2.mp4',
    'Lecture Select.mp4': '58 Interaktywność aplikacji - linku URL_en_2.mp4',
    'Lecture Interactivity of the application - URL.mp4': '59 Konfiguracja z Dasboard_em (URL)_en_2.mp4',
    'Lecture Configuration with Dashboard - URL.mp4': '60 Ankieta - Survey123_en_2.mp4',
    'Lecture Survey - Survey123.mp4': '61 Ankieta - Survey123 - Global_ID_en_2.mp4',
    'Lecture Survey - Survey123 - GlobalID.mp4': '62 Report - Feature Report (Survey123)_en_2.mp4',
    'Lecture Report - Feature Report - Survey123.mp4': '63 Wykres - Chart_en_2.mp4',
    'Lecture Chart.mp4': '64 Wykres - Chart - Dashboard_en_2.mp4',
    'Lecture Chart - Chart - Dashboard.mp4': '65 Wykres - Chart -  Framework_en_2.mp4',
    'Lecture Chart - Chart - Framework.mp4': '66 Zwijanie - Swipe_en_2.mp4',
    'Lecture Rolling - Swipe.mp4': '67 Zwijanie - Swipe - Zakładki - bookmarks_en_2.mp4',
    'Lecture Rolling - Swipe - Tabs - Bookmarks.mp4': '68 Blisko mnie - Near me_en_2.mp4',
    'Lecture Near Me.mp4': '69 Moja lokalizacja - My Location_en_2.mp4',
    'Lecture My Location.mp4': '70 Program modelujący -Suitability Modeler oraz Business Analyst - Usługi - utility_en_2.mp4',
    'Lecture Modeling Program - Suitability Modeler and Business Analyst - Utility Services.mp4': '71 Wskazówki - Directions oraz Drukuj - print_en_2.mp4',
    'Lecture Directions and Print.mp4': '72 Analiza - Analysis_en_2.mp4',
    'Lecture Analysis.mp4': '73 Analiza - Analysis - cd_en_2.mp4',
    'Lecture Analysis - Continued.mp4': '74 Pomiar - Measurement - Współrzędne - Coordinates - Coordinate Conversion_en_2.mp4',
    'Lecture Measurement - Coordinates - Coordinate Conversion.mp4': '76 Skrzynka narzędziowa 3D – Widżet 3D Toolbox - kontroler lotu - Fly Controller_en_2.mp4',
    'Lecture 3D Toolbox - 3D Widget Toolbox - Flight Controller - Fly Controller.mp4': '77 Kontroler widżetu_en_2.mp4',
    'Lecture Widget Controller.mp4': '79 Wyrażenia - wartości dynamicznych_en_2.mp4',
    'Lecture Expressions - Dynamic Text.mp4': '80 Widoki zbudowane na danych_en_2.mp4',
    'Lecture Views.mp4': '82 Tworzenie szablonów_en_2.mp4',
    'Lecture Creating templates.mp4': '83 Ogólnie o szablonach - Pełen ekran - Siatka - Przewijane_en_2.mp4',
    'Lecture Generally about templates - Full screen - Grid - Scrollable.mp4': '85 Install XBLD locally and use it in ArcGIS Online - Server - Client_1_en_2.mp4',
    'Lecture How to Deploy Customized Widgets of XBLD on ArcGIS Online Using AWS.mp4': '86 How to deploy Customised Widgets of XBLD on ArcGIS Online - Locally_en_p_2.mp4',
    'Lecture Install XBLD Locally and Use it in ArcGIS Online - Server - Client.mp4': '87 How to deploy customized widgets of XBLD on ArcGIS Online using AWS_en_2.mp4',
    'Lecture How to Deploy Customized Widgets of XBLD on ArcGIS Online - Locally.mp4': '89 Interfejs – Tryb Express_en_2.mp4',
    'Lecture Interface - Express Mode.mp4': '9 Obsługa interfejsu i Motyw aplikacji_en_2.mp4',
    'Lecture Disconnecting Views - Application Responsiveness - Full Screen - Tablet - Phone.mp4': '90 Rozłączenie widoków – Responsywność aplikacji - Pełny ekran - Tablet - Telefon_en_2.mp4',
    'Lecture Copying widgets between pages.mp4': '91 Kopiowanie widżetów między stronami_en_2.mp4',
    'Lecture Data Update - Truncate - Append.mp4': '92 Aktualizacja danych – Truncate - Append_en_2.mp4',
    'Lecture general – Survey123.mp4': '93 ogólny – Survey123_en_2.mp4'
}

# Sprawdzanie, czy folder istnieje
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Iterowanie po nowoczesnych nazwach
    for new_name, old_name in file_mapping.items():
        new_file_path = os.path.join(folder_path, new_name)
        old_file_path = os.path.join(folder_path, old_name)

        # Sprawdzanie, czy nowy plik istnieje
        if os.path.exists(new_file_path):
            # Przywracanie oryginalnej nazwy pliku
            os.rename(new_file_path, old_file_path)
            print(f"Przywrócono nazwę: '{new_name}' -> '{old_name}'")
        else:
            print(f"Plik '{new_name}' nie istnieje w folderze.")
else:
    print(f"Folder '{folder_path}' nie istnieje lub nie jest folderem.")
