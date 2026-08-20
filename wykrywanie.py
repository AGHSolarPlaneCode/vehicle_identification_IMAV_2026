import cv2
import numpy as np

def classify_vehicle_by_color(image_path):
    # 1. Wczytanie obrazu
    img = cv2.imread(image_path)
    if img is None:
        return "Błąd: Nie można wczytać pliku. Sprawdź ścieżkę.", 0.0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. Zliczamy WSZYSTKIE piksele na wyciętym obrazku (razem z tłem)
    total_pixels = img.shape[0] * img.shape[1]
    
    if total_pixels == 0:
        return "Błąd obrazu", 0.0
    
    # ==========================================
    # 1. MASKI STRAŻACKIE (Tylko Czerwień i Żółć - BEZ BIELI)
    # ==========================================
    
    # Czerwień: Odcinamy rdzę i brąz (Hue 0-8). Saturacja od 120.
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([8, 255, 255])
    lower_red2 = np.array([165, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), 
                              cv2.inRange(hsv, lower_red2, upper_red2))

    # Żółć: Saturacja obniżona do 85 (łapie wyblakłe CCF),
    # ale Hue twardo od 18 w górę (omija całkowicie piaskowy kamuflaż wojskowy!).
    lower_yellow = np.array([18, 85, 120])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Łączymy w maskę strażacką (brak maski białej!)
    mask_firetruck = cv2.bitwise_or(mask_red, mask_yellow)
    firetruck_pixels = cv2.countNonZero(mask_firetruck)

    # ==========================================
    # 2. MASKI WOJSKOWE
    # ==========================================
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255]) 
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Piaskowy: Hue 5 do 17 (Zablokowane przed wejściem w strefę żółci strażackiej).
    lower_sand = np.array([5, 15, 80])
    upper_sand = np.array([17, 100, 255]) 
    mask_sand = cv2.inRange(hsv, lower_sand, upper_sand)

    mask_military = cv2.bitwise_or(mask_green, mask_sand)
    military_pixels = cv2.countNonZero(mask_military)

    # ==========================================
    # 3. LOGIKA KLASYFIKACJI
    # ==========================================
    
    fire_ratio = firetruck_pixels / total_pixels
    
    # Próg 4.5% powstrzyma czerwone kanistry VBL i drobne odblaski, 
    # ale bez problemu wychwyci czerwień i żółć z karoserii CCF/VLTT.
    FIRE_THRESHOLD = 0.045

    if fire_ratio > FIRE_THRESHOLD:
        classification = "Wóz strażacki"
        confidence = min((fire_ratio / 0.15) * 100, 100.0)
    else:
        classification = "Pojazd wojskowy"
        mil_ratio = military_pixels / total_pixels
        confidence = min((mil_ratio / 0.40) * 100, 100.0)

    return classification, round(confidence, 2)

# =========================================
# GŁÓWNA SEKCJA WYKONAWCZA
# ==========================================

plik_wynikowy = "wyniki_klasyfikacji.txt"

# Otwieramy plik do zapisu ("w" tworzy nowy plik lub nadpisuje istniejący)
with open(plik_wynikowy, "w", encoding="utf-8") as f:
    # Ustawienie nagłówka z odpowiednim wyrównaniem kolumn
    # <15 wyrównuje tekst do lewej i rezerwuje 15 miejsc
    # >8 wyrównuje tekst do prawej i rezerwuje 8 miejsc
    naglowek = f"{'Plik':<14} | {'Werdykt':<15} | {'Pewność':>8}"
    separator = "-" * 50
    
    f.write(naglowek + "\n")
    f.write(separator + "\n")
    print(naglowek)
    print(separator)
    pojazdy_strazackie = ["CCF", "VLTT"]
    pojazdy_wojskowe = ["GBC180", "VT4", "VBL"]
    for pojazd in pojazdy_strazackie:
        
        # Pętla od 1 do 11 włącznie
        for x in range(1, 12):
            sciezka_do_pliku = f"E:\Studia\SKN_Solar_Plane\Francja_2026\dataset\strazackie_z_gory\{pojazd}_p_{x}.png"
            nazwa_pliku = f"{pojazd}_p_{x}.png"
            
            # Wywołanie funkcji dla każdego pliku
            klasa, pewnosc = classify_vehicle_by_color(sciezka_do_pliku)
            
            # Przygotowanie tekstu z wynikiem
            linia_wyniku = f"{nazwa_pliku:<14} | {klasa:<15} | {pewnosc:>7}%\n"
            
            # Zapis do pliku
            f.write(linia_wyniku)
            # Wypisanie na ekran, żeby widzieć postęp
            print(linia_wyniku.strip())

        f.write(separator + '\n')
        print(separator)

    for pojazd in pojazdy_wojskowe:
        for x in range(1, 13):
            sciezka_do_pliku = f"E:\Studia\SKN_Solar_Plane\Francja_2026\dataset\wojskowe_z_gory\{pojazd}_p_{x}.png"
            nazwa_pliku = f"{pojazd}_p_{x}.png"
            
            # Wywołanie funkcji dla każdego pliku
            klasa, pewnosc = classify_vehicle_by_color(sciezka_do_pliku)
            
            # Przygotowanie tekstu z wynikiem
            linia_wyniku = f"{nazwa_pliku:<14} | {klasa:<15} | {pewnosc:>7}%\n"
            
            # Zapis do pliku
            f.write(linia_wyniku)
            # Wypisanie na ekran, żeby widzieć postęp
            print(linia_wyniku.strip())

        f.write(separator + '\n')
        print(separator)
        
print(separator)
print(f"Gotowe! Wyniki zostały pomyślnie zapisane w pliku: {plik_wynikowy}")
