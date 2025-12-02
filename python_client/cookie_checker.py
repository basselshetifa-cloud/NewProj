import os
import threading
import tkinter.filedialog as fd
import time
import webbrowser
from collections import defaultdict
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

CHECKERS = {
    "Steam": ["steam", "account_id", "sessionid", "steamid", "steam_login"],
    "Roblox": ["roblox", "rbx", "sessionid", "account_id"],
    "HumbleBundle": ["humblebundle", "humble", "sessionid", "account_id"],
    "PSN": ["psn", "playstation", "sessionid", "account_id"],
    "Genshin": ["genshin", "mihoyo", "sessionid", "account_id"],
    "Tarkov": ["tarkov", "battlestate", "sessionid", "account_id"],
    "FunPay": ["funpay", "sessionid", "account_id"],
    "LinkedIn": ["linkedin", "sessionid", "account_id"],
    "YouTube": ["youtube", "google", "sessionid", "account_id"],
    "Twitch": ["twitch", "sessionid", "account_id"],
    "TikTok": ["tiktok", "sessionid", "account_id"],
    "Instagram": ["instagram", "sessionid", "account_id"],
    "Twitter": ["twitter", "x-csrf-token", "sessionid", "account_id"],
    "Facebook": ["facebook", "c_user", "xs", "account_id"],
    "Amazon": ["amazon", "at-main", "sess-at-main", "sessionid", "account_id"],
    "Netflix": ["netflix", "NetflixId", "SecureNetflixId", "sessionid", "account_id"],
    "Yahoo": ["yahoo", "sessionid", "account_id"],
    "Gmail": ["gmail", "google", "sessionid", "account_id"],
    "Outlook": ["outlook", "live.com", "sessionid", "account_id"],
    "Aol.com": ["aol.com", "sessionid", "account_id"],
    "Rambler.ru": ["rambler.ru", "sessionid", "account_id"],
    "Mail.ru": ["mail.ru", "sessionid", "account_id"],
    "Yandex.ru": ["yandex.ru", "sessionid", "account_id"]
}

NUM_THREADS = 50

class PremiumCookieCheckerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Premium Cookie Checker")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Configure colors
        self.bg_dark = "#23272A"
        self.bg_medium = "#191C1E"
        self.bg_light = "#151718"
        self.text_color = "#FFFFFF"
        self.button_color = "#2ECC71"
        
        self.folder_path = ""
        self.proxy_path = ""
        self.cookies_files = []
        self.proxy_list = []
        self.stop_flag = threading.Event()
        self.pause_flag = threading.Event()
        self.stats = defaultdict(int)
        self.valid_cookies = defaultdict(list)
        self.total_checked = 0
        self.cpm = 0
        self.start_time = 0
        self.lock = threading.Lock()
        self.search_text = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Premium Cookie Checker", 
                                       font=("Segoe UI", 26, "bold"))
        self.title_label.place(x=240, y=8)
        
        # Top buttons frame
        top_buttons_frame = ctk.CTkFrame(self, fg_color=self.bg_medium, height=60)
        top_buttons_frame.place(x=240, y=50, width=950, height=60)
        
        # Top buttons
        btn_width = 140
        btn_height = 40
        btn_y = 10
        
        self.path_logs_btn = ctk.CTkButton(top_buttons_frame, text="PATH LOGS", 
                                          width=btn_width, height=btn_height,
                                          command=self.open_logs_folder)
        self.path_logs_btn.place(x=10, y=btn_y)
        
        self.load_cookies_btn = ctk.CTkButton(top_buttons_frame, text="LOAD COOKIES", 
                                             width=btn_width, height=btn_height,
                                             command=self.load_cookies)
        self.load_cookies_btn.place(x=160, y=btn_y)
        
        self.load_proxy_btn = ctk.CTkButton(top_buttons_frame, text="LOAD PROXY", 
                                           width=btn_width, height=btn_height,
                                           command=self.load_proxy)
        self.load_proxy_btn.place(x=310, y=btn_y)
        
        self.pause_btn = ctk.CTkButton(top_buttons_frame, text="PAUSE", 
                                      width=btn_width, height=btn_height,
                                      command=self.pause_checking)
        self.pause_btn.place(x=460, y=btn_y)
        
        self.stop_btn = ctk.CTkButton(top_buttons_frame, text="STOP", 
                                     width=btn_width, height=btn_height,
                                     fg_color="#E74C3C", hover_color="#C0392B",
                                     command=self.stop_checking)
        self.stop_btn.place(x=610, y=btn_y)
        
        # Left sidebar for stats
        sidebar = ctk.CTkFrame(self, fg_color=self.bg_medium, width=220)
        sidebar.place(x=10, y=50, width=220, height=740)
        
        # Stats labels
        stats_y = 20
        stats_spacing = 50
        
        ctk.CTkLabel(sidebar, text="Statistics", font=("Segoe UI", 18, "bold")).place(x=60, y=stats_y)
        stats_y += 40
        
        ctk.CTkLabel(sidebar, text="All Cookies Files:", anchor="w").place(x=10, y=stats_y)
        self.all_cookies_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.all_cookies_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="Proxy Count:", anchor="w").place(x=10, y=stats_y)
        self.proxy_count_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.proxy_count_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="Remains Check:", anchor="w").place(x=10, y=stats_y)
        self.remains_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.remains_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="Found Cookies:", anchor="w").place(x=10, y=stats_y)
        self.found_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.found_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="Valid Cookies:", anchor="w").place(x=10, y=stats_y)
        self.valid_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.valid_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="Error Networks:", anchor="w").place(x=10, y=stats_y)
        self.errors_label = ctk.CTkLabel(sidebar, text="0", anchor="w", font=("Segoe UI", 12, "bold"))
        self.errors_label.place(x=10, y=stats_y + 20)
        stats_y += stats_spacing
        
        ctk.CTkLabel(sidebar, text="CPM:", anchor="w").place(x=10, y=stats_y)
        self.cpm_label = ctk.CTkLabel(sidebar, text="0", anchor="w", 
                                     font=("Segoe UI", 12, "bold"),
                                     text_color=self.button_color)
        self.cpm_label.place(x=10, y=stats_y + 20)
        
        # Service checkboxes (3 columns)
        services_frame = ctk.CTkFrame(self, fg_color=self.bg_medium)
        services_frame.place(x=240, y=120, width=950, height=200)
        
        ctk.CTkLabel(services_frame, text="Select Services to Check", 
                    font=("Segoe UI", 16, "bold")).place(x=10, y=10)
        
        self.service_vars = {}
        services_list = list(CHECKERS.keys())
        
        # 3 columns layout
        col_width = 310
        start_y = 45
        row_height = 25
        
        for i, service in enumerate(services_list):
            col = i % 3
            row = i // 3
            x = 10 + (col * col_width)
            y = start_y + (row * row_height)
            
            var = ctk.BooleanVar()
            self.service_vars[service] = var
            checkbox = ctk.CTkCheckBox(services_frame, text=service, variable=var,
                                      width=290)
            checkbox.place(x=x, y=y)
        
        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color=self.bg_medium)
        search_frame.place(x=240, y=330, width=950, height=50)
        
        ctk.CTkLabel(search_frame, text="Search:", font=("Segoe UI", 12)).place(x=10, y=13)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=700, placeholder_text="Search in output...")
        self.search_entry.place(x=80, y=10)
        self.search_entry.bind("<KeyRelease>", self.filter_output)
        
        self.clear_search_btn = ctk.CTkButton(search_frame, text="Clear", width=80,
                                             command=self.clear_search)
        self.clear_search_btn.place(x=790, y=10)
        
        # Output text box
        self.output_text = ctk.CTkTextbox(self, width=950, height=340, 
                                         font=("Consolas", 10),
                                         fg_color=self.bg_light)
        self.output_text.place(x=240, y=390)
        
        # START button
        self.start_btn = ctk.CTkButton(self, text="START", width=200, height=50,
                                      font=("Segoe UI", 16, "bold"),
                                      fg_color=self.button_color, 
                                      hover_color="#27AE60",
                                      command=self.start_checking)
        self.start_btn.place(x=990, y=740)
    
    def load_cookies(self):
        folder = fd.askdirectory(title="Select Cookies Folder")
        if folder:
            self.folder_path = folder
            self.cookies_files = []
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    self.cookies_files.append(os.path.join(folder, file))
            
            self.all_cookies_label.configure(text=str(len(self.cookies_files)))
            self.remains_label.configure(text=str(len(self.cookies_files)))
            self.log_output(f"✅ Loaded {len(self.cookies_files)} cookie files from {folder}")
    
    def load_proxy(self):
        file_path = fd.askopenfilename(title="Select Proxy File", 
                                      filetypes=[("Text files", "*.txt")])
        if file_path:
            self.proxy_path = file_path
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.proxy_list = [line.strip() for line in f if line.strip()]
            
            self.proxy_count_label.configure(text=str(len(self.proxy_list)))
            self.log_output(f"✅ Loaded {len(self.proxy_list)} proxies")
    
    def open_logs_folder(self):
        logs_folder = "CookieChecker_Results"
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)
        
        if os.name == 'nt':  # Windows
            os.startfile(logs_folder)
        elif os.name == 'posix':  # macOS/Linux
            webbrowser.open(f"file://{os.path.abspath(logs_folder)}")
    
    def pause_checking(self):
        if self.pause_flag.is_set():
            self.pause_flag.clear()
            self.pause_btn.configure(text="PAUSE")
            self.log_output("▶️ Resumed checking")
        else:
            self.pause_flag.set()
            self.pause_btn.configure(text="RESUME")
            self.log_output("⏸️ Paused checking")
    
    def stop_checking(self):
        self.stop_flag.set()
        self.log_output("🛑 Stopping all checks...")
    
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.search_text = ""
        # Restore full output
        self.output_text.configure(state="normal")
        # Keep existing content
        self.output_text.configure(state="disabled")
    
    def filter_output(self, event=None):
        search = self.search_entry.get().lower()
        self.search_text = search
        # Simple filtering - in real implementation would filter visible content
        # For now just update the search text
    
    def log_output(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def start_checking(self):
        if not self.cookies_files:
            self.log_output("❌ Please load cookie files first!")
            return
        
        # Get selected services
        selected_services = [service for service, var in self.service_vars.items() if var.get()]
        
        if not selected_services:
            self.log_output("❌ Please select at least one service!")
            return
        
        self.stop_flag.clear()
        self.pause_flag.clear()
        self.stats = defaultdict(int)
        self.valid_cookies = defaultdict(list)
        self.total_checked = 0
        self.start_time = time.time()
        
        self.log_output(f"🚀 Starting check for {len(selected_services)} services...")
        self.log_output(f"📁 Total files: {len(self.cookies_files)}")
        
        # Start checking in separate thread
        threading.Thread(target=self.check_cookies, args=(selected_services,), daemon=True).start()
        threading.Thread(target=self.update_cpm, daemon=True).start()
    
    def check_cookies(self, selected_services):
        results_folder = "CookieChecker_Results"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        
        for i, cookie_file in enumerate(self.cookies_files):
            if self.stop_flag.is_set():
                break
            
            while self.pause_flag.is_set():
                time.sleep(0.1)
            
            try:
                with open(cookie_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                
                # Check each selected service
                for service in selected_services:
                    keywords = CHECKERS[service]
                    # Check if any keyword is in the cookie file
                    if any(keyword.lower() in content for keyword in keywords):
                        with self.lock:
                            self.stats[service] += 1
                            self.valid_cookies[service].append(cookie_file)
                        
                        # Save to hits file
                        hits_file = os.path.join(results_folder, f"{service}_hits.txt")
                        with open(hits_file, 'a', encoding='utf-8') as hf:
                            hf.write(f"{cookie_file}\n")
                        
                        self.log_output(f"✅ {service} HIT: {os.path.basename(cookie_file)}")
                
                with self.lock:
                    self.total_checked += 1
                    remaining = len(self.cookies_files) - self.total_checked
                    self.remains_label.configure(text=str(remaining))
                    self.found_label.configure(text=str(self.total_checked))
                    total_hits = sum(self.stats.values())
                    self.valid_label.configure(text=str(total_hits))
            
            except Exception as e:
                with self.lock:
                    self.stats['errors'] += 1
                    self.errors_label.configure(text=str(self.stats['errors']))
                self.log_output(f"❌ Error checking {os.path.basename(cookie_file)}: {str(e)}")
        
        self.log_output("\n🎉 Checking completed!")
        self.log_output(f"📊 Total checked: {self.total_checked}")
        self.log_output(f"✅ Total hits: {sum(self.stats.values())}")
        for service, count in self.stats.items():
            if service != 'errors':
                self.log_output(f"   - {service}: {count}")
    
    def update_cpm(self):
        while not self.stop_flag.is_set():
            time.sleep(1)
            if self.start_time > 0:
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    cpm = int((self.total_checked / elapsed) * 60)
                    self.cpm_label.configure(text=str(cpm))

def main():
    app = PremiumCookieCheckerGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
