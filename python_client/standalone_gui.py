"""
Standalone GUI with High-Performance Engine Options
Supports 4 engines:
1. 🚀 Multi-Process (~1000 CPM) - Maximum speed
2. ⚡ Fast Python (~300 CPM) - Balanced performance
3. 🕵️ Playwright (~80 CPM) - Stealth mode
4. 🌐 Selenium (~40 CPM) - Full browser automation
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
import os
import json
import asyncio

# Import engines
try:
    from fast_engine import FastEngine
    FAST_ENGINE_AVAILABLE = True
except ImportError:
    FAST_ENGINE_AVAILABLE = False

try:
    from performance_checker import PerformanceChecker
    PERF_CHECKER_AVAILABLE = True
except ImportError:
    PERF_CHECKER_AVAILABLE = False

try:
    from stealth_checker import StealthChecker
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False

try:
    from selenium_checker import SeleniumChecker
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from openbullet_editor import OpenBulletEditor
    EDITOR_AVAILABLE = True
except ImportError:
    EDITOR_AVAILABLE = False


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StandaloneGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🔥 Cookie Checker - High Performance Edition")
        self.geometry("1100x750")
        
        self.stealth_checker = StealthChecker() if STEALTH_AVAILABLE else None
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
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, height=80, fg_color="#1a1a1a")
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text="🔥 Cookie Checker - High Performance", 
                    font=("Arial", 24, "bold")).pack(side="left", padx=20)
        
        ctk.CTkLabel(header, text="Standalone Edition", 
                    font=("Arial", 12), text_color="gray").pack(side="left")
        
        if EDITOR_AVAILABLE:
            config_btn = ctk.CTkButton(header, text="⚙️ CONFIG EDITOR", 
                                      command=self.open_config_editor,
                                      width=150, height=40,
                                      fg_color="#2ecc71", hover_color="#27ae60")
            config_btn.pack(side="right", padx=20)
        
        # Main content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left panel - Settings
        left_panel = ctk.CTkFrame(content, width=320)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(left_panel, text="📁 Files", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Cookie file
        ctk.CTkLabel(left_panel, text="Cookie File:").pack(anchor="w", padx=10)
        self.cookie_file_entry = ctk.CTkEntry(left_panel, width=280)
        self.cookie_file_entry.pack(padx=10, pady=5)
        ctk.CTkButton(left_panel, text="Browse", command=self.browse_cookie_file, width=280).pack(padx=10)
        
        # Proxy file
        ctk.CTkLabel(left_panel, text="Proxy File (Optional):").pack(anchor="w", padx=10, pady=(10,0))
        self.proxy_file_entry = ctk.CTkEntry(left_panel, width=280)
        self.proxy_file_entry.pack(padx=10, pady=5)
        ctk.CTkButton(left_panel, text="Browse", command=self.browse_proxy_file, width=280).pack(padx=10)
        
        ctk.CTkLabel(left_panel, text="⚙️ Settings", font=("Arial", 16, "bold")).pack(pady=(20,10))
        
        # Service
        ctk.CTkLabel(left_panel, text="Service:").pack(anchor="w", padx=10)
        self.service_combo = ctk.CTkComboBox(left_panel, values=["Steam", "Discord", "GitHub"], width=280)
        self.service_combo.pack(padx=10, pady=5)
        
        # Threads
        ctk.CTkLabel(left_panel, text="Threads:").pack(anchor="w", padx=10, pady=(10,0))
        self.threads_slider = ctk.CTkSlider(left_panel, from_=1, to=100, number_of_steps=99, width=280)
        self.threads_slider.set(50)
        self.threads_slider.pack(padx=10)
        self.threads_label = ctk.CTkLabel(left_panel, text="50")
        self.threads_label.pack()
        self.threads_slider.configure(command=lambda v: self.threads_label.configure(text=f"{int(v)}"))
        
        # Engine selection
        ctk.CTkLabel(left_panel, text="🔧 Engine Selection:", font=("Arial", 14, "bold")).pack(pady=(15,5))
        
        self.engine_var = ctk.StringVar(value="multiprocess")
        
        # Multi-Process option
        if PERF_CHECKER_AVAILABLE:
            engine_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
            engine_frame.pack(padx=10, fill="x")
            ctk.CTkRadioButton(
                engine_frame, 
                text="🚀 Multi-Process", 
                variable=self.engine_var, 
                value="multiprocess",
                command=self.on_engine_change
            ).pack(side="left")
            ctk.CTkLabel(
                engine_frame,
                text="(~1000 CPM)",
                font=("Arial", 9),
                text_color="#3498db"
            ).pack(side="left", padx=5)
        
        # Fast Python option
        if FAST_ENGINE_AVAILABLE:
            engine_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
            engine_frame.pack(padx=10, fill="x")
            ctk.CTkRadioButton(
                engine_frame,
                text="⚡ Fast Python",
                variable=self.engine_var,
                value="fast",
                command=self.on_engine_change
            ).pack(side="left")
            ctk.CTkLabel(
                engine_frame,
                text="(~300 CPM)",
                font=("Arial", 9),
                text_color="#2ecc71"
            ).pack(side="left", padx=5)
        
        # Playwright option
        if STEALTH_AVAILABLE:
            engine_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
            engine_frame.pack(padx=10, fill="x")
            ctk.CTkRadioButton(
                engine_frame,
                text="🕵️ Playwright",
                variable=self.engine_var,
                value="playwright",
                command=self.on_engine_change
            ).pack(side="left")
            ctk.CTkLabel(
                engine_frame,
                text="(~80 CPM)",
                font=("Arial", 9),
                text_color="#9b59b6"
            ).pack(side="left", padx=5)
        
        # Selenium option
        if SELENIUM_AVAILABLE:
            engine_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
            engine_frame.pack(padx=10, fill="x")
            ctk.CTkRadioButton(
                engine_frame,
                text="🌐 Selenium",
                variable=self.engine_var,
                value="selenium",
                command=self.on_engine_change
            ).pack(side="left")
            ctk.CTkLabel(
                engine_frame,
                text="(~40 CPM)",
                font=("Arial", 9),
                text_color="#e67e22"
            ).pack(side="left", padx=5)
        
        # Selenium options (initially hidden)
        self.selenium_options_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        
        ctk.CTkLabel(self.selenium_options_frame, text="  Browser Mode:", 
                    font=("Arial", 10)).pack(anchor="w", padx=10)
        self.browser_mode_combo = ctk.CTkComboBox(self.selenium_options_frame, 
                                                  values=["Headless", "Headed"], 
                                                  width=260)
        self.browser_mode_combo.set("Headless")
        self.browser_mode_combo.pack(padx=20, pady=2)
        
        self.undetected_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.selenium_options_frame, text="  Undetected ChromeDriver", 
                       variable=self.undetected_var, font=("Arial", 10)).pack(padx=20, pady=2, anchor="w")
        
        # Engine status
        self.engine_status_label = ctk.CTkLabel(
            left_panel, 
            text="🔧 Engine: Multi-Process (Maximum Speed)", 
            font=("Arial", 10), 
            text_color="gray"
        )
        self.engine_status_label.pack(padx=10, pady=(5,0))
        
        # Start button
        self.start_btn = ctk.CTkButton(left_panel, text="▶️ START CHECKING", 
                                       command=self.toggle_checking,
                                       width=280, height=50,
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
    
    def open_config_editor(self):
        if EDITOR_AVAILABLE:
            editor = OpenBulletEditor(self)
            editor.focus()
    
    def on_engine_change(self):
        """Handle engine selection change"""
        engine = self.engine_var.get()
        
        if engine == "multiprocess":
            self.selenium_options_frame.pack_forget()
            self.engine_status_label.configure(text="🔧 Engine: Multi-Process (Maximum Speed)")
        elif engine == "fast":
            self.selenium_options_frame.pack_forget()
            self.engine_status_label.configure(text="🔧 Engine: Fast Python (Balanced)")
        elif engine == "playwright":
            self.selenium_options_frame.pack_forget()
            self.engine_status_label.configure(text="🔧 Engine: Playwright (Stealth)")
        elif engine == "selenium":
            self.selenium_options_frame.pack(padx=10, pady=5)
            self.engine_status_label.configure(text="🔧 Engine: Selenium (Full Browser)")
    
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
        engine = self.engine_var.get()
        
        # Load cookies
        with open(cookie_file, 'r') as f:
            cookies = [line.strip() for line in f if line.strip()]
        
        # Load proxies
        proxies = []
        if proxy_file and os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        
        self.stats['total'] = len(cookies)
        
        # Load config
        try:
            config_path = f'../configs/{service.lower()}.json'
            if not os.path.exists(config_path):
                config_path = f'configs/{service.lower()}.json'
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {e}")
            self.stop_checking()
            return
        
        # Initialize Selenium if needed
        if engine == "selenium" and not self.selenium_checker:
            headless = self.browser_mode_combo.get() == "Headless"
            use_undetected = self.undetected_var.get()
            if SELENIUM_AVAILABLE:
                self.selenium_checker = SeleniumChecker(use_undetected=use_undetected, headless=headless)
        
        # Run checks based on engine
        if engine == "multiprocess" and PERF_CHECKER_AVAILABLE:
            self.run_multiprocess(config, cookies, proxies)
        elif engine == "fast" and FAST_ENGINE_AVAILABLE:
            self.run_fast_python(config, cookies, proxies, num_threads)
        elif engine == "playwright" and STEALTH_AVAILABLE:
            self.run_playwright(service, cookies, proxies, num_threads)
        elif engine == "selenium" and SELENIUM_AVAILABLE:
            self.run_selenium(service, cookies, proxies)
        else:
            messagebox.showerror("Error", f"Engine '{engine}' not available")
            self.stop_checking()
            return
        
        # Cleanup
        if engine == "selenium" and self.selenium_checker:
            self.selenium_checker.close()
            self.selenium_checker = None
        
        self.stop_checking()
        messagebox.showinfo("Complete", f"Checking complete!\n\nHits: {self.stats['hits']}\nBad: {self.stats['bad']}")
    
    def run_multiprocess(self, config, cookies, proxies):
        """Run checks using multi-process engine"""
        try:
            checker = PerformanceChecker(threads_per_process=50)
            results = checker.check_cookies(config, cookies, proxies if proxies else None)
            
            # Process results
            for i, result in enumerate(results):
                if not self.checking:
                    break
                
                self.process_result(cookies[i], result)
                
        except Exception as e:
            self.log_message(f"⚠️ Multi-process error: {e}")
    
    def run_fast_python(self, config, cookies, proxies, num_threads):
        """Run checks using fast async engine"""
        try:
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_async():
                async with FastEngine() as engine:
                    results = await engine.check_batch(
                        config, 
                        cookies, 
                        proxies if proxies else None,
                        max_concurrent=num_threads
                    )
                    return results
            
            results = loop.run_until_complete(run_async())
            loop.close()
            
            # Process results
            for i, result in enumerate(results):
                if not self.checking:
                    break
                
                self.process_result(cookies[i], result)
                
        except Exception as e:
            self.log_message(f"⚠️ Fast Python error: {e}")
    
    def run_playwright(self, service, cookies, proxies, num_threads):
        """Run checks using Playwright stealth engine"""
        from concurrent.futures import ThreadPoolExecutor
        
        with ThreadPoolExecutor(max_workers=min(num_threads, 20)) as executor:
            for i, cookie in enumerate(cookies):
                if not self.checking:
                    break
                
                proxy = proxies[i % len(proxies)] if proxies else ""
                executor.submit(self.check_playwright, service, cookie, proxy)
    
    def run_selenium(self, service, cookies, proxies):
        """Run checks using Selenium"""
        for i, cookie in enumerate(cookies):
            if not self.checking:
                break
            
            proxy = proxies[i % len(proxies)] if proxies else ""
            self.check_selenium(service, cookie, proxy)
    
    def check_playwright(self, service, cookie, proxy):
        """Check single cookie with Playwright"""
        try:
            response = self.stealth_checker.check(service, "", cookie, proxy)
            self.process_result(cookie, self.response_to_dict(response))
        except Exception as e:
            self.stats['errors'] += 1
            self.log_message(f"⚠️ Error: {str(e)}")
            self.update_stats()
    
    def check_selenium(self, service, cookie, proxy):
        """Check single cookie with Selenium"""
        try:
            response = self.selenium_checker.check(service, "", cookie, proxy)
            self.process_result(cookie, self.response_to_dict(response))
        except Exception as e:
            self.stats['errors'] += 1
            self.log_message(f"⚠️ Error: {str(e)}")
            self.update_stats()
    
    def response_to_dict(self, response):
        """Convert response object to dict"""
        if hasattr(response, '__dict__'):
            return {
                'valid': response.valid,
                'status_code': getattr(response, 'status_code', 0),
                'check_time': getattr(response, 'check_time', 0.0),
                'extracted_data': getattr(response, 'extracted_data', '{}')
            }
        return response
    
    def process_result(self, cookie, result):
        """Process a single result"""
        self.stats['checked'] += 1
        
        if result.get('valid', False):
            self.stats['hits'] += 1
            self.log_result("✅ HIT", cookie, result, self.hits_text)
        else:
            self.stats['bad'] += 1
            self.log_result("❌ BAD", cookie, result, self.bad_text)
        
        self.log_result("📝", cookie, result, self.all_text)
        
        self.update_stats()
        self.update_progress()
    
    def log_result(self, status, cookie, result, textbox):
        msg = f"{status} | {cookie[:50]}... | "
        if result:
            check_time = result.get('check_time', 0.0)
            msg += f"Time: {check_time:.2f}s"
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
    import multiprocessing as mp
    mp.freeze_support()  # Required for Windows multiprocessing
    
    app = StandaloneGUI()
    app.mainloop()
