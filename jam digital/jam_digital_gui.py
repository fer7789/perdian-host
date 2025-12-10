import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import locale

# Set locale ke Indonesia
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia.1252')
    except:
        pass

class JamDigital:
    def __init__(self, root):
        self.root = root
        self.root.title("Jam Digital Global - Fake GPS")
        self.root.geometry("1200x700")
        self.root.configure(bg='#667eea')
        
        self.is_12_hour = False
        self.is_dark = False
        self.timezone_offset = 7  # Default: WIB
        
        # Database kota dengan timezone
        self.cities = {
            # 38 Provinsi Indonesia
            "Aceh (WIB)": 7,
            "Sumatera Utara (WIB)": 7,
            "Sumatera Barat (WIB)": 7,
            "Riau (WIB)": 7,
            "Kepulauan Riau (WIB)": 7,
            "Jambi (WIB)": 7,
            "Sumatera Selatan (WIB)": 7,
            "Bangka Belitung (WIB)": 7,
            "Bengkulu (WIB)": 7,
            "Lampung (WIB)": 7,
            "DKI Jakarta (WIB)": 7,
            "Banten (WIB)": 7,
            "Jawa Barat (WIB)": 7,
            "Jawa Tengah (WIB)": 7,
            "DI Yogyakarta (WIB)": 7,
            "Jawa Timur (WIB)": 7,
            "Kalimantan Barat (WIB)": 7,
            "Kalimantan Tengah (WIB)": 7,
            "Kalimantan Selatan (WITA)": 8,
            "Kalimantan Timur (WITA)": 8,
            "Kalimantan Utara (WITA)": 8,
            "Bali (WITA)": 8,
            "Nusa Tenggara Barat (WITA)": 8,
            "Nusa Tenggara Timur (WITA)": 8,
            "Sulawesi Utara (WITA)": 8,
            "Sulawesi Tengah (WITA)": 8,
            "Sulawesi Selatan (WITA)": 8,
            "Sulawesi Tenggara (WITA)": 8,
            "Sulawesi Barat (WITA)": 8,
            "Gorontalo (WITA)": 8,
            "Maluku (WIT)": 9,
            "Maluku Utara (WIT)": 9,
            "Papua (WIT)": 9,
            "Papua Barat (WIT)": 9,
            "Papua Tengah (WIT)": 9,
            "Papua Pegunungan (WIT)": 9,
            "Papua Selatan (WIT)": 9,
            "Papua Barat Daya (WIT)": 9,
            
            # Kota Besar Indonesia
            "Jakarta": 7,
            "Surabaya": 7,
            "Bandung": 7,
            "Medan": 7,
            "Semarang": 7,
            "Makassar": 8,
            "Palembang": 7,
            "Tangerang": 7,
            "Depok": 7,
            "Bekasi": 7,
            "Bogor": 7,
            "Batam": 7,
            "Pekanbaru": 7,
            "Bandar Lampung": 7,
            "Malang": 7,
            "Padang": 7,
            "Denpasar": 8,
            "Samarinda": 8,
            "Banjarmasin": 8,
            "Balikpapan": 8,
            "Manado": 8,
            "Pontianak": 7,
            "Jayapura": 9,
            
            # Asia Tenggara
            "Singapura": 8,
            "Bangkok, Thailand": 7,
            "Kuala Lumpur, Malaysia": 8,
            "Manila, Filipina": 8,
            "Hanoi, Vietnam": 7,
            "Yangon, Myanmar": 6.5,
            "Phnom Penh, Kamboja": 7,
            "Vientiane, Laos": 7,
            "Bandar Seri Begawan, Brunei": 8,
            "Dili, Timor Leste": 9,
            
            # Asia Timur
            "Tokyo, Jepang": 9,
            "Seoul, Korea Selatan": 9,
            "Beijing, China": 8,
            "Hong Kong": 8,
            "Taipei, Taiwan": 8,
            "Pyongyang, Korea Utara": 9,
            
            # Asia Selatan
            "New Delhi, India": 5.5,
            "Mumbai, India": 5.5,
            "Dhaka, Bangladesh": 6,
            "Islamabad, Pakistan": 5,
            "Kathmandu, Nepal": 5.75,
            "Colombo, Sri Lanka": 5.5,
            
            # Timur Tengah
            "Dubai, UAE": 4,
            "Riyadh, Arab Saudi": 3,
            "Istanbul, Turki": 3,
            "Tehran, Iran": 3.5,
            "Doha, Qatar": 3,
            "Kuwait City, Kuwait": 3,
            "Baghdad, Irak": 3,
            "Yerusalem, Israel": 2,
            
            # Eropa
            "London, Inggris": 0,
            "Paris, Prancis": 1,
            "Berlin, Jerman": 1,
            "Roma, Italia": 1,
            "Madrid, Spanyol": 1,
            "Amsterdam, Belanda": 1,
            "Moskow, Rusia": 3,
            "Athena, Yunani": 2,
            "Vienna, Austria": 1,
            "Brussels, Belgia": 1,
            
            # Afrika
            "Kairo, Mesir": 2,
            "Lagos, Nigeria": 1,
            "Johannesburg, Afrika Selatan": 2,
            "Nairobi, Kenya": 3,
            "Casablanca, Maroko": 1,
            
            # Amerika
            "New York, AS": -5,
            "Los Angeles, AS": -8,
            "Chicago, AS": -6,
            "Houston, AS": -6,
            "Miami, AS": -5,
            "Toronto, Kanada": -5,
            "Vancouver, Kanada": -8,
            "Mexico City, Meksiko": -6,
            "Havana, Kuba": -5,
            "Sao Paulo, Brasil": -3,
            "Rio de Janeiro, Brasil": -3,
            "Buenos Aires, Argentina": -3,
            "Lima, Peru": -5,
            "Bogota, Kolombia": -5,
            
            # Oceania
            "Sydney, Australia": 11,
            "Melbourne, Australia": 11,
            "Brisbane, Australia": 10,
            "Perth, Australia": 8,
            "Auckland, Selandia Baru": 13,
            "Wellington, Selandia Baru": 13,
            "Suva, Fiji": 12,
        }
        
        self.current_city = "DKI Jakarta (WIB)"
        
        # Container utama dengan 2 kolom
        main_container = tk.Frame(root, bg='#667eea')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== PANEL KIRI: JAM DIGITAL =====
        left_panel = tk.Frame(main_container, bg='#667eea', width=600)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header Panel Kiri
        tk.Label(
            left_panel,
            text="⏰ JAM DIGITAL",
            font=('Arial', 28, 'bold'),
            fg='white',
            bg='#667eea'
        ).pack(pady=20)
        
        # Emoji Lokasi
        self.location_emoji = tk.Label(
            left_panel,
            text="📍",
            font=('Arial', 40),
            bg='#667eea'
        )
        self.location_emoji.pack(pady=10)
        
        # Label Nama Kota
        self.city_label = tk.Label(
            left_panel,
            text=self.current_city,
            font=('Arial', 26, 'bold'),
            fg='#FFD700',
            bg='#667eea'
        )
        self.city_label.pack(pady=10)
        
        # Label Waktu (Besar)
        self.time_label = tk.Label(
            left_panel, 
            font=('Arial', 80, 'bold'),
            fg='white',
            bg='#667eea'
        )
        self.time_label.pack(pady=30)
        
        # Label Tanggal
        self.date_label = tk.Label(
            left_panel,
            font=('Arial', 22),
            fg='white',
            bg='#667eea'
        )
        self.date_label.pack(pady=15)
        
        # Tombol Pengaturan
        settings_frame = tk.Frame(left_panel, bg='#667eea')
        settings_frame.pack(pady=30)
        
        self.format_button = tk.Button(
            settings_frame,
            text="12 Jam",
            font=('Arial', 16, 'bold'),
            command=self.toggle_format,
            bg='white',
            fg='#667eea',
            padx=25,
            pady=12,
            border=0,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.format_button.pack(side=tk.LEFT, padx=10)
        
        self.theme_button = tk.Button(
            settings_frame,
            text="🌙 Mode Gelap",
            font=('Arial', 16, 'bold'),
            command=self.toggle_theme,
            bg='white',
            fg='#667eea',
            padx=25,
            pady=12,
            border=0,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.theme_button.pack(side=tk.LEFT, padx=10)
        
        # ===== PANEL KANAN: FAKE GPS =====
        right_panel = tk.Frame(main_container, bg='#4a5fc1', width=600)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header Panel Kanan
        tk.Label(
            right_panel,
            text="🌍 FAKE GPS",
            font=('Arial', 28, 'bold'),
            fg='white',
            bg='#4a5fc1'
        ).pack(pady=20)
        
        tk.Label(
            right_panel,
            text="Pilih lokasi untuk melihat waktu setempat",
            font=('Arial', 14),
            fg='#E0E0E0',
            bg='#4a5fc1'
        ).pack(pady=5)
        
        # Frame Zona Indonesia
        indo_frame = tk.Frame(right_panel, bg='#4a5fc1')
        indo_frame.pack(pady=20)
        
        tk.Label(
            indo_frame,
            text="⚡ Zona Indonesia:",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#4a5fc1'
        ).pack(pady=10)
        
        indo_buttons = tk.Frame(indo_frame, bg='#4a5fc1')
        indo_buttons.pack()
        
        self.wib_button = tk.Button(
            indo_buttons,
            text="WIB",
            font=('Arial', 14, 'bold'),
            command=lambda: self.set_city("DKI Jakarta (WIB)"),
            bg='#FFD700',
            fg='#4a5fc1',
            padx=20,
            pady=10,
            border=0,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.wib_button.pack(side=tk.LEFT, padx=5)
        
        self.wita_button = tk.Button(
            indo_buttons,
            text="WITA",
            font=('Arial', 14),
            command=lambda: self.set_city("Bali (WITA)"),
            bg='white',
            fg='#4a5fc1',
            padx=20,
            pady=10,
            border=0,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.wita_button.pack(side=tk.LEFT, padx=5)
        
        self.wit_button = tk.Button(
            indo_buttons,
            text="WIT",
            font=('Arial', 14),
            command=lambda: self.set_city("Papua (WIT)"),
            bg='white',
            fg='#4a5fc1',
            padx=20,
            pady=10,
            border=0,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.wit_button.pack(side=tk.LEFT, padx=5)
        
        city_select_frame = tk.Frame(right_panel, bg='#4a5fc1')
        city_select_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(
            city_select_frame,
            text="🔍 Cari Lokasi:",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#4a5fc1'
        ).pack(pady=10)
        
        self.city_var = tk.StringVar(value=self.current_city)
        self.city_dropdown = ttk.Combobox(
            city_select_frame,
            textvariable=self.city_var,
            values=sorted(self.cities.keys()),
            font=('Arial', 14),
            state='readonly',
            width=35
        )
        self.city_dropdown.pack(pady=10)
        self.city_dropdown.bind('<<ComboboxSelected>>', self.change_city)
        
        # Info Zona Waktu
        info_frame = tk.Frame(right_panel, bg='#3d4fa3', relief=tk.GROOVE, borderwidth=2)
        info_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(
            info_frame,
            text="📊 Informasi Zona Waktu",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#3d4fa3'
        ).pack(pady=15)
        
        self.timezone_info = tk.Label(
            info_frame,
            text="UTC +7:00",
            font=('Arial', 24, 'bold'),
            fg='#FFD700',
            bg='#3d4fa3'
        )
        self.timezone_info.pack(pady=10)
        
        tk.Label(
            info_frame,
            text="Total Lokasi Tersedia:",
            font=('Arial', 14),
            fg='#E0E0E0',
            bg='#3d4fa3'
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text=f"{len(self.cities)} Kota",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#3d4fa3'
        ).pack(pady=5)
        
        tk.Label(
            info_frame,
            text="• 38 Provinsi Indonesia\n• Kota-kota Besar Dunia\n• Update Real-Time",
            font=('Arial', 12),
            fg='#E0E0E0',
            bg='#3d4fa3',
            justify=tk.LEFT
        ).pack(pady=15)
        
        # Mulai update jam
        self.update_clock()
    
    def change_city(self, event=None):
        """Mengubah kota dari dropdown"""
        city = self.city_var.get()
        self.set_city(city)
    
    def set_city(self, city):
        """Mengatur kota dan timezone"""
        self.current_city = city
        self.timezone_offset = self.cities[city]
        self.city_label.config(text=city)
        self.city_var.set(city)
        
        # Update info zona waktu
        if self.timezone_offset >= 0:
            sign = "+"
        else:
            sign = ""
        
        hours = int(self.timezone_offset)
        minutes = int((self.timezone_offset - hours) * 60)
        if minutes > 0:
            self.timezone_info.config(text=f"UTC {sign}{hours}:{minutes:02d}")
        else:
            self.timezone_info.config(text=f"UTC {sign}{hours}:00")
        
        self.wib_button.config(bg='white', font=('Arial', 14))
        self.wita_button.config(bg='white', font=('Arial', 14))
        self.wit_button.config(bg='white', font=('Arial', 14))
        
        # Cek apakah kota termasuk WIB, WITA, atau WIT
        if "(WIB)" in city or self.timezone_offset == 7:
            self.wib_button.config(bg='#FFD700', font=('Arial', 14, 'bold'))
        elif "(WITA)" in city or self.timezone_offset == 8:
            self.wita_button.config(bg='#FFD700', font=('Arial', 14, 'bold'))
        elif "(WIT)" in city or self.timezone_offset == 9:
            self.wit_button.config(bg='#FFD700', font=('Arial', 14, 'bold'))
        
        self.update_clock()
    
    def toggle_format(self):
        """Toggle antara format 12 dan 24 jam"""
        self.is_12_hour = not self.is_12_hour
        self.format_button.config(text="24 Jam" if self.is_12_hour else "12 Jam")
        self.update_clock()
    
    def toggle_theme(self):
        """Toggle antara mode terang dan gelap"""
        self.is_dark = not self.is_dark
        
        if self.is_dark:
            left_bg = '#1e3c72'
            right_bg = '#2a4d8f'
            info_bg = '#1e3557'
            self.theme_button.config(text="☀️ Mode Terang")
        else:
            left_bg = '#667eea'
            right_bg = '#4a5fc1'
            info_bg = '#3d4fa3'
            self.theme_button.config(text="🌙 Mode Gelap")
        
        # Update warna panel kiri
        self.root.configure(bg=left_bg)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                # Panel kiri
                if widget.winfo_children()[0].winfo_children():
                    first_child = widget.winfo_children()[0]
                    if hasattr(first_child, 'cget'):
                        try:
                            text = first_child.cget('text')
                            if '⏰' in str(text):
                                self.update_panel_colors(widget, left_bg)
                            elif '🌍' in str(text):
                                self.update_panel_colors(widget, right_bg, info_bg)
                        except:
                            pass
        
        self.location_emoji.configure(bg=left_bg)
        self.city_label.configure(bg=left_bg)
        self.time_label.configure(bg=left_bg)
        self.date_label.configure(bg=left_bg)
    
    def update_panel_colors(self, panel, bg_color, info_bg=None):
        """Update warna panel dan semua widget di dalamnya"""
        panel.configure(bg=bg_color)
        for widget in panel.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label)):
                if info_bg and isinstance(widget, tk.Frame) and widget.cget('relief') == tk.GROOVE:
                    widget.configure(bg=info_bg)
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg=info_bg)
                else:
                    try:
                        widget.configure(bg=bg_color)
                    except:
                        pass
                if hasattr(widget, 'winfo_children'):
                    self.update_panel_colors(widget, bg_color, info_bg)
    
    def update_clock(self):
        """Update waktu setiap detik"""
        # Waktu UTC
        utc_now = datetime.utcnow()
        
        # Offset zona waktu
        now = utc_now + timedelta(hours=self.timezone_offset)
        
        # Format waktu
        jam = now.hour
        menit = now.minute
        detik = now.second
        
        if self.is_12_hour:
            ampm = 'PM' if jam >= 12 else 'AM'
            jam = jam % 12 if jam % 12 != 0 else 12
            time_string = f"{jam:02d}:{menit:02d}:{detik:02d} {ampm}"
        else:
            time_string = f"{jam:02d}:{menit:02d}:{detik:02d}"
        
        # Format tanggal
        try:
            date_string = now.strftime("%A, %d %B %Y")
        except:
            hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
            bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                     'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
            date_string = f"{hari[now.weekday()]}, {now.day} {bulan[now.month-1]} {now.year}"
        
        # Update label
        self.time_label.config(text=time_string)
        self.date_label.config(text=date_string)
        
        # Update setiap 1000ms (1 detik)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = JamDigital(root)
    root.mainloop()