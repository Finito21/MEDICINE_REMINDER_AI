import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import threading
import time
import os
import re
from tkinter import font

class MedicineReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💊 Aplikacja Przypomnień o Lekach")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Ustawienia stylu
        self.setup_styles()
        
        # Dane aplikacji
        self.medicines = []
        self.reminder_thread = None
        self.stop_reminder = False
        self.data_file = "medicines.json"
        self.last_reminder_time = {}  # Śledzenie ostatnich przypomnień
        
        # Wczytaj dane
        self.load_medicines()
        
        # Utwórz interfejs
        self.create_widgets()
        
        # Uruchom wątek przypomnień
        self.start_reminder_thread()
        
        # Obsługa zamknięcia aplikacji
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrowanie okna
        self.center_window()
    
    def center_window(self):
        """Centrowanie okna na ekranie"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Konfiguracja stylów aplikacji"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Konfiguracja kolorów i stylów
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'), 
                       foreground='#2c3e50',
                       background='#ecf0f1')
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#34495e')
        
        style.configure('Success.TButton', 
                       background='#27ae60',
                       foreground='white')
        
        style.configure('Warning.TButton', 
                       background='#f39c12',
                       foreground='white')
        
        style.configure('Danger.TButton', 
                       background='#e74c3c',
                       foreground='white')
        
        style.configure('Info.TButton', 
                       background='#3498db',
                       foreground='white')
        
        # Styl dla tabeli
        style.configure('Treeview', 
                       font=('Segoe UI', 10),
                       rowheight=30)
        
        style.configure('Treeview.Heading', 
                       font=('Segoe UI', 10, 'bold'))
    
    def create_widgets(self):
        """Tworzenie interfejsu użytkownika"""
        # Główny kontener
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfiguracja grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Tytuł z ikoną
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(title_frame, text="💊 Aplikacja Przypomnień o Lekach", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2)
        
        # Statystyki
        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky=(tk.W, tk.E))
        
        self.stats_var = tk.StringVar()
        self.update_stats()
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, 
                               style='Header.TLabel')
        stats_label.pack(side=tk.LEFT)
        
        # Przyciski akcji
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 15), sticky=(tk.W, tk.E))
        
        # Przyciski z ikonami i stylami
        ttk.Button(button_frame, text="➕ Dodaj Lek", 
                  command=self.add_medicine_dialog,
                  style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="✏️ Edytuj Lek", 
                  command=self.edit_medicine_dialog,
                  style='Info.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🗑️ Usuń Lek", 
                  command=self.delete_medicine_dialog,
                  style='Danger.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Odśwież", 
                  command=self.refresh_table,
                  style='Warning.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # Tabela leków
        self.create_medicine_table(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Gotowy - Aplikacja działa poprawnie")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
    
    def update_stats(self):
        """Aktualizacja statystyk"""
        total = len(self.medicines)
        due_today = sum(1 for m in self.medicines if self.get_medicine_status(m) == "Do przyjęcia")
        self.stats_var.set(f"📊 Statystyki: {total} leków | {due_today} do przyjęcia dzisiaj")
    
    def create_medicine_table(self, parent):
        """Tworzenie tabeli leków"""
        # Kontener dla tabeli
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Tabela
        columns = ('Nazwa', 'Dawkowanie', 'Częstotliwość', 'Godzina', 'Status', 'Ostatnie przyjęcie')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Konfiguracja kolumn
        self.tree.heading('Nazwa', text='💊 Nazwa leku')
        self.tree.heading('Dawkowanie', text='💊 Dawkowanie')
        self.tree.heading('Częstotliwość', text='⏰ Częstotliwość')
        self.tree.heading('Godzina', text='🕐 Godzina przyjęcia')
        self.tree.heading('Status', text='📋 Status')
        self.tree.heading('Ostatnie przyjęcie', text='📅 Ostatnie przyjęcie')
        
        self.tree.column('Nazwa', width=200, minwidth=150)
        self.tree.column('Dawkowanie', width=150, minwidth=100)
        self.tree.column('Częstotliwość', width=120, minwidth=100)
        self.tree.column('Godzina', width=100, minwidth=80)
        self.tree.column('Status', width=100, minwidth=80)
        self.tree.column('Ostatnie przyjęcie', width=150, minwidth=120)
        
        # Scrollbary
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Podwójne kliknięcie do edycji
        self.tree.bind('<Double-1>', lambda e: self.edit_medicine_dialog())
        
        # Pojedyncze kliknięcie do zaznaczenia
        self.tree.bind('<Button-1>', self.on_tree_select)
        
        # Aktualizuj tabelę
        self.refresh_table()
    
    def on_tree_select(self, event):
        """Obsługa zaznaczenia w tabeli"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            medicine_name = item['values'][0]
            self.status_var.set(f"📋 Wybrano: {medicine_name}")
    
    def refresh_table(self):
        """Odświeżanie tabeli leków"""
        # Wyczyść tabelę
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Dodaj leki do tabeli
        for medicine in self.medicines:
            status = self.get_medicine_status(medicine)
            last_taken = medicine.get('last_taken', 'Brak danych')
            
            # Kolorowanie wierszy na podstawie statusu
            tags = ()
            if status == "Do przyjęcia":
                tags = ('urgent',)
            elif status == "Oczekuje":
                tags = ('waiting',)
            
            self.tree.insert('', tk.END, values=(
                medicine['name'],
                medicine['dosage'],
                medicine['frequency'],
                medicine['time'],
                status,
                last_taken
            ), tags=tags)
        
        # Konfiguracja kolorów
        self.tree.tag_configure('urgent', background='#ffebee')
        self.tree.tag_configure('waiting', background='#f3e5f5')
        
        # Aktualizuj statystyki
        self.update_stats()
    
    def get_medicine_status(self, medicine):
        """Określa status leku"""
        current_time = datetime.datetime.now().time()
        medicine_time = datetime.datetime.strptime(medicine['time'], '%H:%M').time()
        
        if current_time >= medicine_time:
            return "Do przyjęcia"
        else:
            return "Oczekuje"
    
    def add_medicine_dialog(self):
        """Dialog dodawania leku"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Dodaj nowy lek")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centrowanie okna
        self.center_dialog(dialog)
        
        # Zmienne
        name_var = tk.StringVar()
        dosage_var = tk.StringVar()
        frequency_var = tk.StringVar()
        time_var = tk.StringVar()
        
        # Interfejs
        ttk.Label(dialog, text="➕ Dodaj nowy lek", 
                 style='Header.TLabel').pack(pady=15)
        
        # Formularz
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Nazwa leku
        ttk.Label(form_frame, text="💊 Nazwa leku:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=8)
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=35, font=('Segoe UI', 10))
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Dawkowanie
        ttk.Label(form_frame, text="💊 Dawkowanie:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=8)
        dosage_entry = ttk.Entry(form_frame, textvariable=dosage_var, width=35, font=('Segoe UI', 10))
        dosage_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Częstotliwość
        ttk.Label(form_frame, text="⏰ Częstotliwość:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=8)
        frequency_combo = ttk.Combobox(form_frame, textvariable=frequency_var, 
                                     values=['Codziennie', 'Co 12 godzin', 'Co 8 godzin', 'Co 6 godzin', 'Raz w tygodniu'],
                                     font=('Segoe UI', 10), width=32)
        frequency_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        frequency_combo.set('Codziennie')
        
        # Godzina
        ttk.Label(form_frame, text="🕐 Godzina (HH:MM):", 
                 font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=8)
        time_entry = ttk.Entry(form_frame, textvariable=time_var, width=35, font=('Segoe UI', 10))
        time_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Konfiguracja grid
        form_frame.columnconfigure(1, weight=1)
        
        # Przyciski
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=25, pady=15)
        
        def save_medicine():
            if self.validate_medicine_data(name_var.get(), dosage_var.get(), 
                                         frequency_var.get(), time_var.get()):
                medicine = {
                    'name': name_var.get().strip(),
                    'dosage': dosage_var.get().strip(),
                    'frequency': frequency_var.get(),
                    'time': time_var.get(),
                    'added_date': datetime.datetime.now().isoformat(),
                    'last_taken': 'Brak danych'
                }
                self.medicines.append(medicine)
                self.save_medicines()
                self.refresh_table()
                self.status_var.set(f"✅ Dodano lek: {medicine['name']}")
                dialog.destroy()
        
        ttk.Button(button_frame, text="💾 Zapisz", 
                  command=save_medicine, style='Success.TButton').pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="❌ Anuluj", 
                  command=dialog.destroy, style='Danger.TButton').pack(side=tk.RIGHT)
        
        # Fokus na pierwsze pole
        name_entry.focus()
    
    def center_dialog(self, dialog):
        """Centrowanie okna dialogowego"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_rootx() + self.root.winfo_width() // 2) - (width // 2)
        y = (self.root.winfo_rooty() + self.root.winfo_height() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def edit_medicine_dialog(self):
        """Dialog edycji leku"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Wybierz lek do edycji")
            return
        
        # Pobierz wybrany lek
        item = self.tree.item(selection[0])
        medicine_name = item['values'][0]
        medicine = next((m for m in self.medicines if m['name'] == medicine_name), None)
        
        if not medicine:
            messagebox.showerror("❌ Błąd", "Nie znaleziono leku")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Edytuj lek")
        dialog.geometry("450x350")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centrowanie okna
        self.center_dialog(dialog)
        
        # Zmienne
        name_var = tk.StringVar(value=medicine['name'])
        dosage_var = tk.StringVar(value=medicine['dosage'])
        frequency_var = tk.StringVar(value=medicine['frequency'])
        time_var = tk.StringVar(value=medicine['time'])
        
        # Interfejs
        ttk.Label(dialog, text="✏️ Edytuj lek", 
                 style='Header.TLabel').pack(pady=15)
        
        # Formularz
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Nazwa leku
        ttk.Label(form_frame, text="💊 Nazwa leku:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=8)
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=35, font=('Segoe UI', 10))
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Dawkowanie
        ttk.Label(form_frame, text="💊 Dawkowanie:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=8)
        dosage_entry = ttk.Entry(form_frame, textvariable=dosage_var, width=35, font=('Segoe UI', 10))
        dosage_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Częstotliwość
        ttk.Label(form_frame, text="⏰ Częstotliwość:", 
                 font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=8)
        frequency_combo = ttk.Combobox(form_frame, textvariable=frequency_var, 
                                     values=['Codziennie', 'Co 12 godzin', 'Co 8 godzin', 'Co 6 godzin', 'Raz w tygodniu'],
                                     font=('Segoe UI', 10), width=32)
        frequency_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Godzina
        ttk.Label(form_frame, text="🕐 Godzina (HH:MM):", 
                 font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=8)
        time_entry = ttk.Entry(form_frame, textvariable=time_var, width=35, font=('Segoe UI', 10))
        time_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # Konfiguracja grid
        form_frame.columnconfigure(1, weight=1)
        
        # Przyciski
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=25, pady=15)
        
        def save_changes():
            if self.validate_medicine_data(name_var.get(), dosage_var.get(), 
                                         frequency_var.get(), time_var.get()):
                medicine['name'] = name_var.get().strip()
                medicine['dosage'] = dosage_var.get().strip()
                medicine['frequency'] = frequency_var.get()
                medicine['time'] = time_var.get()
                
                self.save_medicines()
                self.refresh_table()
                self.status_var.set(f"✅ Zaktualizowano lek: {medicine['name']}")
                dialog.destroy()
        
        ttk.Button(button_frame, text="💾 Zapisz", 
                  command=save_changes, style='Success.TButton').pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="❌ Anuluj", 
                  command=dialog.destroy, style='Danger.TButton').pack(side=tk.RIGHT)
    
    def delete_medicine_dialog(self):
        """Dialog usuwania leku"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Ostrzeżenie", "Wybierz lek do usunięcia")
            return
        
        # Pobierz wybrany lek
        item = self.tree.item(selection[0])
        medicine_name = item['values'][0]
        
        # Potwierdzenie usunięcia
        result = messagebox.askyesno("🗑️ Potwierdzenie", 
                                   f"Czy na pewno chcesz usunąć lek '{medicine_name}'?\n\nTa operacja nie może być cofnięta.")
        
        if result:
            self.medicines = [m for m in self.medicines if m['name'] != medicine_name]
            self.save_medicines()
            self.refresh_table()
            self.status_var.set(f"🗑️ Usunięto lek: {medicine_name}")
    
    def validate_medicine_data(self, name, dosage, frequency, time_str):
        """Walidacja danych leku"""
        errors = []
        
        if not name or not name.strip():
            errors.append("❌ Nazwa leku nie może być pusta")
        
        if not dosage or not dosage.strip():
            errors.append("❌ Dawkowanie nie może być puste")
        
        if not frequency:
            errors.append("❌ Wybierz częstotliwość")
        
        # Walidacja formatu czasu
        if not time_str:
            errors.append("❌ Godzina nie może być pusta")
        else:
            time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
            if not time_pattern.match(time_str):
                errors.append("❌ Nieprawidłowy format godziny (użyj HH:MM, np. 08:30)")
        
        if errors:
            messagebox.showerror("❌ Błąd walidacji", "\n".join(errors))
            return False
        
        return True
    
    def load_medicines(self):
        """Wczytywanie leków z pliku"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.medicines = json.load(f)
        except Exception as e:
            messagebox.showerror("❌ Błąd", f"Nie udało się wczytać danych:\n{str(e)}")
            self.medicines = []
    
    def save_medicines(self):
        """Zapisywanie leków do pliku"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.medicines, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("❌ Błąd", f"Nie udało się zapisać danych:\n{str(e)}")
    
    def start_reminder_thread(self):
        """Uruchomienie wątku przypomnień"""
        self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
        self.reminder_thread.start()
    
    def reminder_loop(self):
        """Pętla sprawdzająca przypomnienia"""
        while not self.stop_reminder:
            current_time = datetime.datetime.now()
            
            for medicine in self.medicines:
                try:
                    medicine_time = datetime.datetime.strptime(medicine['time'], '%H:%M').time()
                    current_time_only = current_time.time()
                    
                    # Sprawdź czy to czas na lek (z tolerancją 1 minuty)
                    time_diff = abs((current_time_only.hour * 60 + current_time_only.minute) - 
                                  (medicine_time.hour * 60 + medicine_time.minute))
                    
                    # Sprawdź czy nie było już przypomnienia dla tego leku w tej godzinie
                    reminder_key = f"{medicine['name']}_{current_time.strftime('%Y-%m-%d_%H')}"
                    
                    if time_diff <= 1 and reminder_key not in self.last_reminder_time:
                        self.show_reminder(medicine)
                        self.last_reminder_time[reminder_key] = current_time
                        
                except Exception as e:
                    print(f"Błąd podczas sprawdzania przypomnienia: {e}")
            
            # Sprawdzaj co minutę
            time.sleep(60)
    
    def show_reminder(self, medicine):
        """Wyświetlanie przypomnienia"""
        try:
            # Powiadomienie w aplikacji
            self.root.after(0, lambda: messagebox.showinfo(
                "⏰ Przypomnienie o leku",
                f"💊 Pora na lek: {medicine['name']}\n\n"
                f"💊 Dawkowanie: {medicine['dosage']}\n"
                f"⏰ Godzina: {medicine['time']}\n\n"
                f"Czy przyjąłeś/aś już lek?"
            ))
            
            # Aktualizuj status w interfejsie
            self.root.after(0, lambda: self.status_var.set(f"⏰ Przypomnienie: {medicine['name']}"))
            self.root.after(0, self.refresh_table)
            
        except Exception as e:
            print(f"Błąd podczas wyświetlania przypomnienia: {e}")
    
    def on_closing(self):
        """Obsługa zamknięcia aplikacji"""
        self.stop_reminder = True
        self.root.destroy()

def main():
    """Główna funkcja aplikacji"""
    try:
        root = tk.Tk()
        app = MedicineReminderApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("❌ Błąd krytyczny", f"Aplikacja napotkała błąd:\n{str(e)}")

if __name__ == "__main__":
    main() 