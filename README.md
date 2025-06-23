# Aplikacja Przypomnień o Lekach

Nowoczesna aplikacja desktopowa do zarządzania harmonogramem przyjmowania leków z automatycznymi przypomnieniami.

## Funkcjonalności

- **Wyświetlanie leków** - Czytelna tabela z wszystkimi zapisanymi lekami
- **Dodawanie leku** - Formularz z walidacją danych
- **Edycja leku** - Możliwość modyfikacji istniejących wpisów
- **Usuwanie leku** - Bezpieczne usuwanie z potwierdzeniem
- **Automatyczne przypomnienia** - Powiadomienia o porze przyjęcia leku

## Wymagania systemowe

- Python 3.7 lub nowszy
- Windows 10/11 (testowane)
- Biblioteki: tkinter (wbudowana), plyer

## Instalacja

1. Sklonuj lub pobierz projekt
2. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie

```bash
python main.py
```

## Użytkowanie

### Dodawanie leku
1. Kliknij przycisk "Dodaj Lek"
2. Wypełnij formularz:
   - **Nazwa leku** - Nazwa leku (wymagane)
   - **Dawkowanie** - Ilość i forma leku (wymagane)
   - **Częstotliwość** - Jak często przyjmować lek
   - **Godzina** - Format HH:MM (np. 08:30)
3. Kliknij "Zapisz"

### Edycja leku
1. Wybierz lek z tabeli (pojedyncze kliknięcie)
2. Kliknij "Edytuj Lek" lub użyj podwójnego kliknięcia
3. Zmodyfikuj dane
4. Kliknij "Zapisz"

### Usuwanie leku
1. Wybierz lek z tabeli
2. Kliknij "Usuń Lek"
3. Potwierdź usunięcie

### Przypomnienia
- Aplikacja automatycznie sprawdza czas co minutę
- Gdy nadejdzie pora na lek, pojawi się powiadomienie
- Status leku w tabeli automatycznie się aktualizuje

## Bezpieczeństwo

- Wszystkie dane są walidowane przed zapisem
- Usuwanie wymaga potwierdzenia
- Dane są zapisywane lokalnie w formacie JSON
- Obsługa błędów i wyjątków

## Struktura plików

```
MEDICINE_REMINDER_AI/
├── main.py              # Główny plik aplikacji
├── requirements.txt     # Zależności Python
├── README.md           # Ten plik
└── medicines.json      # Plik z danymi (tworzony automatycznie)
```

## Rozwiązywanie problemów

### Aplikacja nie uruchamia się
- Sprawdź czy masz zainstalowany Python 3.7+
- Upewnij się, że wszystkie zależności są zainstalowane

### Przypomnienia nie działają
- Sprawdź czy aplikacja ma uprawnienia do wyświetlania powiadomień
- Upewnij się, że godzina jest w formacie HH:MM

### Dane nie zapisują się
- Sprawdź uprawnienia do zapisu w katalogu aplikacji
- Upewnij się, że plik medicines.json nie jest używany przez inną aplikację

## Licencja

Ten projekt jest dostępny na licencji MIT. 