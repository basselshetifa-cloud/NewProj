import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os
from grpc_client import GRPCClient
from stealth_checker import StealthChecker
from selenium_checker import SeleniumChecker
from openbullet_editor import OpenBulletEditor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CookieCheckerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔥 Hybrid Cookie Checker - YashvirGaming")
        self.geometry("1000x700")
        
        self.grpc_client = None
        self.stealth_checker = StealthChecker()
        self.selenium_checker = None
        self.checking = False
        self.threads = []
        
        self.stats = {
            'total': 0,
            'checked': 0,
            'hits': 0,
            'bad': 0,
            'errors': 0,
            'cpm': 0,
            'start_time': None
        }
        
        self.setup_ui()
        self.connect_grpc()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, height=80, fg_color="#1a1a1a")
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="🔥 Hybrid Cookie Checker", 
                    font=("Arial", 24, "bold")).pack(side="left", padx=20)
        
        ctk.CTkLabel(header, text="Go Backend + Python Stealth", 
                    font=("Arial", 12), text_color="gray").pack(side="left")
        
        config_btn = ctk.CTkButton(header, text="⚙️ CONFIG EDITOR", 
                                  command=self.open_config_editor,
                                  width=150, height=40,
                                  fg_color="#2ecc71", hover_color="#27ae60")
        config_btn.pack(side="right", padx=20)
        
        # Main content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left panel - Settings
        left_panel = ctk.CTkFrame(content, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(left_panel, text="📁 Files", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Cookie file
        ctk.CTkLabel(left_panel, text="Cookie File:").pack(anchor="w", padx=10)
        self.cookie_file_entry = ctk.CTkEntry(left_panel, width=260)
        self.cookie_file_entry.pack(padx=10, pady=5)
        ctk.CTkButton(left_panel, text="Browse", command=self.browse_cookie_file, width=260).pack(padx=10)
        
        # Proxy file
        ctk.CTkLabel(left_panel, text="Proxy File (Optional):").pack(anchor="w", padx=10, pady=(10,0))
        self.proxy_file_entry = ctk.CTkEntry(left_panel, width=260)
        self.proxy_file_entry.pack(padx=10, pady=5)
        ctk.CTkButton(left_panel, text="Browse", command=self.browse_proxy_file, width=260).pack(padx=10)
        
        ctk.CTkLabel(left_panel, text="⚙️ Settings", font=("Arial", 16, "bold")).pack(pady=(20,10))
        
        # Service
        ctk.CTkLabel(left_panel, text="Service:").pack(anchor="w", padx=10)
        self.service_combo = ctk.CTkComboBox(left_panel, values=["Steam", "Discord", "GitHub"], width=260)
        self.service_combo.pack(padx=10, pady=5)
        
        # Threads
        ctk.CTkLabel(left_panel, text="Threads:").pack(anchor="w", padx=10, pady=(10,0))
        self.threads_slider = ctk.CTkSlider(left_panel, from_=1, to=100, number_of_steps=99, width=260)
        self.threads_slider.set(10)
        self.threads_slider.pack(padx=10)
        self.threads_label = ctk.CTkLabel(left_panel, text="10")
        self.threads_label.pack()
        self.threads_slider.configure(command=lambda v: self.threads_label.configure(text=f"{int(v)}"))
        
        # Stealth mode
        self.stealth_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(left_panel, text="🕵️ Use Stealth Mode (Playwright)", 
                       variable=self.stealth_var, command=self.on_stealth_toggle).pack(padx=10, pady=(10,0))
        
        # Selenium mode
        self.selenium_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(left_panel, text="🌐 Use Selenium (Chrome)", 
                       variable=self.selenium_var, command=self.on_selenium_toggle).pack(padx=10, pady=(5,0))
        
        # Selenium options (initially hidden)
        self.selenium_options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        
        ctk.CTkLabel(self.selenium_options_frame, text="  Browser Mode:", 
                    font=("Arial", 10)).pack(anchor="w", padx=10)
        self.browser_mode_combo = ctk.CTkComboBox(self.selenium_options_frame, 
                                                  values=["Headless", "Headed"], 
                                                  width=240)
        self.browser_mode_combo.set("Headless")
        self.browser_mode_combo.pack(padx=20, pady=2)
        
        self.undetected_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.selenium_options_frame, text="  Undetected ChromeDriver", 
                       variable=self.undetected_var, font=("Arial", 10)).pack(padx=20, pady=2, anchor="w")
        
        # Engine status indicator
        self.engine_status_label = ctk.CTkLabel(left_panel, text="🔧 Engine: Go", 
                                               font=("Arial", 10), text_color="gray")
        self.engine_status_label.pack(padx=10, pady=(5,0))

        
        # Start button
        self.start_btn = ctk.CTkButton(left_panel, text="▶️ START CHECKING", 
                                       command=self.toggle_checking,
                                       width=260, height=50,
                                       fg_color="#27ae60", hover_color="#229954",
                                       font=("Arial", 14, "bold"))
        self.start_btn.pack(padx=10, pady=20)
        
        # Right panel - Results
        right_panel = ctk.CTkFrame(content)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Stats
        stats_frame = ctk.CTkFrame(right_panel, height=120)
        stats_frame.pack(fill="x", padx=10, pady=10)
        stats_frame.pack_propagate(False)
        
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(expand=True)
        
        self.stat_labels = {}
        stats = [
            ("📊 Total", "total", "white"),
            ("✅ Hits", "hits", "#2ecc71"),
            ("❌ Bad", "bad", "#e74c3c"),
            ("⚡ CPM", "cpm", "#3498db"),
            ("⚠️ Errors", "errors", "#f39c12")
        ]
        
        for i, (label, key, color) in enumerate(stats):
            frame = ctk.CTkFrame(stats_grid, fg_color="transparent")
            frame.grid(row=0, column=i, padx=10)
            
            ctk.CTkLabel(frame, text=label, font=("Arial", 12)).pack()
            lbl = ctk.CTkLabel(frame, text="0", font=("Arial", 20, "bold"), text_color=color)
            lbl.pack()
            self.stat_labels[key] = lbl
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(right_panel, width=300)
        self.progress.pack(padx=10, pady=5)
        self.progress.set(0)
        
        # Results tabs
        self.tabview = ctk.CTkTabview(right_panel)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("✅ Hits")
        self.tabview.add("❌ Bad")
        self.tabview.add("📝 All Results")
        
        self.hits_text = ctk.CTkTextbox(self.tabview.tab("✅ Hits"), wrap="word")
        self.hits_text.pack(fill="both", expand=True)
        
        self.bad_text = ctk.CTkTextbox(self.tabview.tab("❌ Bad"), wrap="word")
        self.bad_text.pack(fill="both", expand=True)
        
        self.all_text = ctk.CTkTextbox(self.tabview.tab("📝 All Results"), wrap="word")
        self.all_text.pack(fill="both", expand=True)
    
    def connect_grpc(self):
        try:
            self.grpc_client = GRPCClient()
            self.log_message("✅ Connected to Go gRPC Server")
        except Exception as e:
            self.log_message(f"⚠️ gRPC connection failed: {e}")
            messagebox.showwarning("Warning", "Go server not running. Only stealth mode will work.")
    
    def open_config_editor(self):
        editor = OpenBulletEditor(self)
        editor.focus()
    
    def on_stealth_toggle(self):
        """Handle stealth mode toggle"""
        if self.stealth_var.get():
            self.selenium_var.set(False)
            self.selenium_options_frame.pack_forget()
            self.engine_status_label.configure(text="🔧 Engine: Playwright (Stealth)")
        else:
            self.engine_status_label.configure(text="🔧 Engine: Go")
    
    def on_selenium_toggle(self):
        """Handle Selenium mode toggle"""
        if self.selenium_var.get():
            self.stealth_var.set(False)
            self.selenium_options_frame.pack(padx=10, pady=5)
            self.engine_status_label.configure(text="🔧 Engine: Selenium (Chrome)")
        else:
            self.selenium_options_frame.pack_forget()
            self.engine_status_label.configure(text="🔧 Engine: Go")

    
    def browse_cookie_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.cookie_file_entry.delete(0, "end")
            self.cookie_file_entry.insert(0, file_path)
    
    def browse_proxy_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.proxy_file_entry.delete(0, "end")
            self.proxy_file_entry.insert(0, file_path)
    
    def toggle_checking(self):
        if not self.checking:
            self.start_checking()
        else:
            self.stop_checking()
    
    def start_checking(self):
        cookie_file = self.cookie_file_entry.get()
        if not cookie_file or not os.path.exists(cookie_file):
            messagebox.showerror("Error", "Please select a valid cookie file")
            return
        
        self.checking = True
        self.start_btn.configure(text="⏸️ STOP", fg_color="#e74c3c", hover_color="#c0392b")
        
        self.stats = {
            'total': 0,
            'checked': 0,
            'hits': 0,
            'bad': 0,
            'errors': 0,
            'cpm': 0,
            'start_time': time.time()
        }
        
        self.update_stats()
        
        thread = threading.Thread(target=self.run_checker, daemon=True)
        thread.start()
    
    def stop_checking(self):
        self.checking = False
        self.start_btn.configure(text="▶️ START CHECKING", fg_color="#27ae60", hover_color="#229954")
    
    def run_checker(self):
        cookie_file = self.cookie_file_entry.get()
        proxy_file = self.proxy_file_entry.get()
        service = self.service_combo.get()
        num_threads = int(self.threads_slider.get())
        use_stealth = self.stealth_var.get()
        use_selenium = self.selenium_var.get()
        
        # Initialize Selenium checker if needed
        if use_selenium and not self.selenium_checker:
            headless = self.browser_mode_combo.get() == "Headless"
            use_undetected = self.undetected_var.get()
            self.selenium_checker = SeleniumChecker(use_undetected=use_undetected, headless=headless)
        
        with open(cookie_file, 'r') as f:
            cookies = [line.strip() for line in f if line.strip()]
        
        proxies = []
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        
        self.stats['total'] = len(cookies)
        
        from concurrent.futures import ThreadPoolExecutor
        
        # Reduce threads for Selenium (it's more resource-intensive)
        max_workers = 1 if use_selenium else num_threads
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, cookie in enumerate(cookies):
                if not self.checking:
                    break
                
                proxy = proxies[i % len(proxies)] if proxies else ""
                executor.submit(self.check_cookie, service, cookie, proxy, use_stealth, use_selenium)
        
        # Cleanup Selenium
        if use_selenium and self.selenium_checker:
            self.selenium_checker.close()
            self.selenium_checker = None
        
        self.stop_checking()
        messagebox.showinfo("Complete", f"Checking complete!\n\nHits: {self.stats['hits']}\nBad: {self.stats['bad']}")
    
    def check_cookie(self, service, cookie, proxy, use_stealth, use_selenium):
        try:
            if use_selenium:
                response = self.selenium_checker.check(service, "", cookie, proxy)
            elif use_stealth or not self.grpc_client:
                response = self.stealth_checker.check(service, "", cookie, proxy)
            else:
                response = self.grpc_client.check_cookie(service, "", cookie, proxy, use_stealth)
            
            self.stats['checked'] += 1
            
            if response and response.valid:
                self.stats['hits'] += 1
                self.log_result("✅ HIT", cookie, response, self.hits_text)
            else:
                self.stats['bad'] += 1
                self.log_result("❌ BAD", cookie, response, self.bad_text)
            
            self.log_result("📝", cookie, response, self.all_text)
            
        except Exception as e:
            self.stats['errors'] += 1
            self.log_message(f"⚠️ Error: {str(e)}")
        
        self.update_stats()
        self.update_progress()
    
    def log_result(self, status, cookie, response, textbox):
        msg = f"{status} | {cookie[:50]}... | "
        if response:
            msg += f"Time: {response.check_time:.2f}s"
        msg += "\n"
        
        self.after(0, lambda: textbox.insert("end", msg))
    
    def log_message(self, message):
        self.after(0, lambda: self.all_text.insert("end", f"{message}\n"))
    
    def update_stats(self):
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                self.stats['cpm'] = int((self.stats['checked'] / elapsed) * 60)
        
        self.stat_labels['total'].configure(text=str(self.stats['total']))
        self.stat_labels['hits'].configure(text=str(self.stats['hits']))
        self.stat_labels['bad'].configure(text=str(self.stats['bad']))
        self.stat_labels['cpm'].configure(text=str(self.stats['cpm']))
        self.stat_labels['errors'].configure(text=str(self.stats['errors']))
    
    def update_progress(self):
        if self.stats['total'] > 0:
            progress = self.stats['checked'] / self.stats['total']
            self.progress.set(progress)

if __name__ == "__main__":
    app = CookieCheckerGUI()
    app.mainloop()