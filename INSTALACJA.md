# Instrukcja Instalacji i Uruchomienia

## Wymagania systemowe

- **Python 3.7 lub nowszy** (zalecane Python 3.8+)
- **Windows 10/11** (testowane)
- **Minimalne wymagania sprzętowe:**
  - 2 GB RAM
  - 100 MB wolnego miejsca na dysku
  - Rozdzielczość ekranu: 800x600 lub wyższa

## Instalacja Python

1. **Pobierz Python** ze strony oficjalnej: https://www.python.org/downloads/
2. **Zainstaluj Python** z zaznaczoną opcją "Add Python to PATH"
3. **Sprawdź instalację** otwierając wiersz poleceń i wpisując:
   ```bash
   python --version
   ```

## Uruchomienie aplikacji

### Metoda 1: Bezpośrednie uruchomienie
1. Otwórz wiersz poleceń (cmd) lub PowerShell
2. Przejdź do katalogu z aplikacją:
   ```bash
   cd C:\ścieżka\do\MEDICINE_REMINDER_AI
   ```
3. Uruchom aplikację:
   ```bash
   python main.py
   ```

### Metoda 2: Podwójne kliknięcie
1. Kliknij prawym przyciskiem myszy na plik `main.py`
2. Wybierz "Otwórz za pomocą" → "Python"

### Metoda 3: Skrót na pulpicie
1. Kliknij prawym przyciskiem myszy na plik `main.py`
2. Wybierz "Utwórz skrót"
3. Przenieś skrót na pulpit
4. Kliknij dwukrotnie na skrót

## Rozwiązywanie problemów

### Problem: "python nie jest rozpoznawane jako polecenie"
**Rozwiązanie:**
1. Sprawdź czy Python jest zainstalowany: `python --version`
2. Jeśli nie działa, spróbuj: `py --version`
3. Jeśli nadal nie działa, dodaj Python do zmiennej PATH

### Problem: "No module named 'tkinter'"
**Rozwiązanie:**
1. Tkinter powinien być wbudowany w Python
2. Jeśli brakuje, zainstaluj ponownie Python z zaznaczoną opcją "tcl/tk and IDLE"

### Problem: Aplikacja nie uruchamia się
**Rozwiązanie:**
1. Sprawdź czy wszystkie pliki są w tym samym katalogu
2. Uruchom z wiersza poleceń, aby zobaczyć błędy
3. Sprawdź czy masz uprawnienia do zapisu w katalogu

### Problem: Przypomnienia nie działają
**Rozwiązanie:**
1. Sprawdź czy aplikacja ma uprawnienia do wyświetlania powiadomień
2. Upewnij się, że godzina jest w formacie HH:MM (np. 08:30)
3. Sprawdź czy system nie blokuje powiadomień

## Bezpieczeństwo

- Aplikacja działa lokalnie na Twoim komputerze
- Dane są przechowywane w pliku `medicines.json` w katalogu aplikacji
- Brak połączenia z internetem
- Wszystkie dane są szyfrowane i bezpieczne

## Wsparcie techniczne

Jeśli napotkasz problemy:
1. Sprawdź plik `README.md` w katalogu aplikacji
2. Uruchom aplikację z wiersza poleceń, aby zobaczyć szczegółowe błędy
3. Sprawdź czy wszystkie pliki są obecne w katalogu

## Aktualizacje

Aplikacja jest samodzielna i nie wymaga aktualizacji. Wszystkie funkcje są wbudowane w kod źródłowy. 