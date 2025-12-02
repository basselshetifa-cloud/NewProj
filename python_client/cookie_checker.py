import os
import threading
import tkinter.filedialog as fd
import time
import webbrowser
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

NUM_THREADS = 50

class PremiumCookieCheckerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cookie Checker")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Configure colors
        self.bg_dark = "#23272A"
        self.bg_medium = "#191C1E"
        self.bg_light = "#151718"
        self.text_color = "#FFFFFF"
        self.button_color = "#009965"
        
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
        
        # Load configs dynamically
        self.configs = self.load_configs()
        self.config_vars = {}
        self.config_count_labels = {}
        
        self.setup_ui()
    
    def load_configs(self):
        """Load config files dynamically from configs folder"""
        configs = {}
        # Try both configs/ and ../configs/
        folder = "configs" if os.path.exists("configs") else "../configs"
        
        if not os.path.exists(folder):
            # Can't log yet, UI not setup
            return configs
        
        for file in os.listdir(folder):
            if file.endswith(('.json', '.loli')):
                # Create clean config name
                name = file.replace('.json', '').replace('.loli', '').replace('_', ' ').title()
                configs[name] = {
                    'path': os.path.join(folder, file),
                    'keywords': self.extract_keywords(os.path.join(folder, file))
                }
        
        return configs
    
    def extract_keywords(self, config_path):
        """Extract keywords from config file for simple checking"""
        keywords = []
        try:
            with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Try to parse as JSON
                try:
                    data = json.loads(content)
                    # Extract common keyword patterns
                    if 'name' in data:
                        keywords.append(data['name'].lower())
                    if 'service' in data:
                        keywords.append(data['service'].lower())
                    if 'keywords' in data:
                        keywords.extend([k.lower() for k in data['keywords']])
                except json.JSONDecodeError:
                    # For .loli files or invalid JSON, extract from filename
                    pass
                
                # If no keywords found, use filename as keyword
                if not keywords:
                    filename = os.path.basename(config_path)
                    base_name = filename.replace('.json', '').replace('.loli', '').lower()
                    # Use set to avoid duplicates
                    keyword_set = {base_name, base_name.replace('_', ''), base_name.replace(' ', '')}
                    keywords = list(keyword_set)
        except Exception as e:
            # Fallback to filename
            filename = os.path.basename(config_path)
            base_name = filename.replace('.json', '').replace('.loli', '').lower()
            keywords = [base_name]
        
        return keywords
    
    def setup_ui(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="Cookie Checker", 
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
        
        # Service checkboxes (4 columns)
        services_frame = ctk.CTkFrame(self, fg_color=self.bg_dark)
        services_frame.place(x=240, y=120, width=950, height=200)
        
        ctk.CTkLabel(services_frame, text="Select Configs to Check", 
                    font=("Segoe UI", 16, "bold")).place(x=10, y=10)
        
        # 4 columns layout for configs
        config_names = list(self.configs.keys())
        col_width = 230
        start_y = 45
        row_height = 25
        
        for i, config_name in enumerate(config_names):
            col = i % 4  # 4 columns
            row = i // 4
            x = 10 + (col * col_width)
            y = start_y + (row * row_height)
            
            var = ctk.BooleanVar()
            self.config_vars[config_name] = var
            
            # Create frame for checkbox and count
            config_frame = ctk.CTkFrame(services_frame, fg_color="transparent")
            config_frame.place(x=x, y=y, width=220, height=25)
            
            checkbox = ctk.CTkCheckBox(config_frame, text=f"{config_name}: ", 
                                      variable=var, width=180)
            checkbox.pack(side="left")
            
            count_label = ctk.CTkLabel(config_frame, text="0", 
                                      font=("Segoe UI", 10, "bold"))
            count_label.pack(side="left")
            self.config_count_labels[config_name] = count_label
        
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
                                         font=("Consolas", 14),
                                         fg_color=self.bg_light)
        self.output_text.place(x=240, y=390)
        
        # START button
        self.start_btn = ctk.CTkButton(self, text="START", width=200, height=50,
                                      font=("Segoe UI", 16, "bold"),
                                      fg_color=self.button_color, 
                                      hover_color="#00805A",
                                      command=self.start_checking)
        self.start_btn.place(x=990, y=740)
    
    def load_cookies(self):
        """Load cookie files from user-selected folder (GUI dialog ensures safe path)"""
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
        """Clear search and restore full output"""
        self.search_entry.delete(0, 'end')
        self.search_text = ""
    
    def filter_output(self, event=None):
        """Filter output based on search text"""
        search = self.search_entry.get().lower()
        if not search:
            return
        
        # Get all text
        self.output_text.configure(state="normal")
        full_text = self.output_text.get("1.0", "end")
        
        # Filter lines containing search text
        filtered_lines = [line for line in full_text.split('\n') if search in line.lower()]
        
        # Update display
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", '\n'.join(filtered_lines))
        self.output_text.configure(state="disabled")
    
    def log_output(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", message + "\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def start_checking(self):
        if not self.cookies_files:
            self.log_output("❌ Please load cookie files first!")
            return
        
        # Get selected configs
        selected_configs = [config for config, var in self.config_vars.items() if var.get()]
        
        if not selected_configs:
            self.log_output("❌ Please select at least one config!")
            return
        
        self.stop_flag.clear()
        self.pause_flag.clear()
        self.stats = defaultdict(int)
        self.valid_cookies = defaultdict(list)
        self.total_checked = 0
        self.start_time = time.time()
        
        self.log_output(f"🚀 Starting check for {len(selected_configs)} configs...")
        self.log_output(f"📁 Total files: {len(self.cookies_files)}")
        self.log_output(f"⚡ Using {NUM_THREADS} threads with keyword matching...")
        
        # Start checking in separate thread
        threading.Thread(target=self.check_cookies, args=(selected_configs,), daemon=True).start()
        threading.Thread(target=self.update_cpm, daemon=True).start()
    
    def check_cookies(self, selected_configs):
        results_folder = "CookieChecker_Results"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        
        # Use ThreadPoolExecutor for multi-threading
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = []
            for cookie_file in self.cookies_files:
                if self.stop_flag.is_set():
                    break
                future = executor.submit(self.check_cookie_file, cookie_file, selected_configs, results_folder)
                futures.append(future)
            
            # Wait for all to complete
            for future in futures:
                if self.stop_flag.is_set():
                    break
                try:
                    future.result()
                except Exception as e:
                    with self.lock:
                        self.stats['errors'] += 1
                        self.errors_label.configure(text=str(self.stats['errors']))
                    self.log_output(f"❌ Error in thread: {str(e)}")
        
        self.log_output("\n🎉 Checking completed!")
        self.log_output(f"📊 Total checked: {self.total_checked}")
        self.log_output(f"✅ Total hits: {sum(self.stats.values())}")
        for config, count in self.stats.items():
            if config != 'errors':
                self.log_output(f"   - {config}: {count}")
    
    def check_cookie_file(self, cookie_file, selected_configs, results_folder):
        """Check a single cookie file against selected configs"""
        while self.pause_flag.is_set():
            time.sleep(0.1)
        
        if self.stop_flag.is_set():
            return
        
        try:
            with open(cookie_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # Check each selected config
            for config_name in selected_configs:
                config = self.configs[config_name]
                keywords = config['keywords']
                
                # Check if any keyword is in the cookie file (keywords already lowercased)
                if any(keyword in content for keyword in keywords):
                    with self.lock:
                        self.stats[config_name] += 1
                        self.valid_cookies[config_name].append(cookie_file)
                        
                        # Update config count in UI
                        if config_name in self.config_count_labels:
                            self.config_count_labels[config_name].configure(
                                text=str(self.stats[config_name])
                            )
                    
                    # Save to hits file in config-specific folder
                    # Sanitize config name for filesystem
                    safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in config_name)
                    config_folder = os.path.join(results_folder, safe_name.replace(' ', '_'))
                    os.makedirs(config_folder, exist_ok=True)
                    hits_file = os.path.join(config_folder, "hits.txt")
                    
                    with open(hits_file, 'a', encoding='utf-8') as hf:
                        hf.write(f"{cookie_file}\n")
                    
                    self.log_output(f"✅ {config_name} HIT: {os.path.basename(cookie_file)}")
            
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
