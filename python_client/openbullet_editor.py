import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os


class OpenBulletEditor(ctk.CTkToplevel):
    """
    Complete OpenBullet-style visual config editor with all block types:
    - REQUEST, PARSE, KEYCHECK, FUNCTION, UTILITY
    - CAPTCHA, TCP, BYPASS CF (Cloudflare)
    - BROWSER ACTION, ELEMENT ACTION, EXECUTE JS, NAVIGATE
    """
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("⚙️ OpenBullet Config Editor - Advanced")
        self.geometry("1400x900")
        
        self.config_data = {
            'name': '',
            'author': 'YashvirGaming',
            'version': '1.0',
            'url': '',
            'method': 'GET',
            'cookie_format': 'netscape',
            'needs_stealth': False,
            'use_selenium': False,
            'browser_mode': 'headless',
            'timeout': 15,
            'blocks': []
        }
        
        self.block_types = [
            "REQUEST", "PARSE", "KEYCHECK", "FUNCTION", "UTILITY",
            "CAPTCHA", "TCP", "BYPASS_CF", "BROWSER_ACTION", 
            "ELEMENT_ACTION", "EXECUTE_JS", "NAVIGATE"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top bar
        top_bar = ctk.CTkFrame(main_container, height=50, fg_color="#1a1a1a")
        top_bar.pack(fill="x", padx=5, pady=5)
        top_bar.pack_propagate(False)
        
        ctk.CTkLabel(top_bar, text="⚙️ OpenBullet Config Editor", 
                    font=("Arial", 18, "bold")).pack(side="left", padx=10)
        
        ctk.CTkButton(top_bar, text="💾 Save Config", command=self.save_config,
                     width=120, fg_color="#27ae60").pack(side="right", padx=5)
        ctk.CTkButton(top_bar, text="📂 Load Config", command=self.load_config,
                     width=120, fg_color="#3498db").pack(side="right", padx=5)
        ctk.CTkButton(top_bar, text="👁️ Preview JSON", command=self.preview_json,
                     width=120, fg_color="#9b59b6").pack(side="right", padx=5)
        
        # Split into left (config info) and right (blocks)
        content = ctk.CTkFrame(main_container)
        content.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel - Config Info
        left_panel = ctk.CTkScrollableFrame(content, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 5))
        left_panel.pack_propagate(False)
        
        ctk.CTkLabel(left_panel, text="📋 Config Information", 
                    font=("Arial", 14, "bold")).pack(pady=10)
        
        # Config fields
        self.name_entry = self.create_field(left_panel, "Config Name:")
        self.author_entry = self.create_field(left_panel, "Author:")
        self.author_entry.insert(0, "YashvirGaming")
        self.version_entry = self.create_field(left_panel, "Version:")
        self.version_entry.insert(0, "1.0")
        self.url_entry = self.create_field(left_panel, "Target URL:")
        
        self.method_combo = self.create_combo(left_panel, "HTTP Method:", 
                                              ["GET", "POST", "PUT", "DELETE"])
        self.cookie_format_combo = self.create_combo(left_panel, "Cookie Format:", 
                                                     ["json", "netscape", "header"])
        
        # Checkboxes
        self.stealth_var = ctk.BooleanVar()
        ctk.CTkCheckBox(left_panel, text="Needs Stealth (Playwright)", 
                       variable=self.stealth_var).pack(pady=5, padx=10, anchor="w")
        
        self.selenium_var = ctk.BooleanVar()
        ctk.CTkCheckBox(left_panel, text="Use Selenium (Chrome)", 
                       variable=self.selenium_var).pack(pady=5, padx=10, anchor="w")
        
        self.browser_mode_combo = self.create_combo(left_panel, "Browser Mode:", 
                                                    ["headless", "headed"])
        
        self.timeout_entry = self.create_field(left_panel, "Timeout (seconds):")
        self.timeout_entry.insert(0, "15")
        
        # Right panel - Blocks
        right_panel = ctk.CTkFrame(content)
        right_panel.pack(side="left", fill="both", expand=True)
        
        # Blocks header
        blocks_header = ctk.CTkFrame(right_panel, height=60)
        blocks_header.pack(fill="x", padx=5, pady=5)
        blocks_header.pack_propagate(False)
        
        ctk.CTkLabel(blocks_header, text="🧩 Blocks", 
                    font=("Arial", 14, "bold")).pack(side="left", padx=10)
        
        # Block type selector
        ctk.CTkLabel(blocks_header, text="Add Block:").pack(side="left", padx=5)
        self.block_type_combo = ctk.CTkComboBox(blocks_header, values=self.block_types, 
                                               width=150)
        self.block_type_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(blocks_header, text="➕ Add Block", command=self.add_block,
                     width=100, fg_color="#2ecc71").pack(side="left", padx=5)
        
        # Blocks list
        self.blocks_frame = ctk.CTkScrollableFrame(right_panel)
        self.blocks_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.block_widgets = []
    
    def create_field(self, parent, label):
        """Create labeled entry field"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame, text=label, anchor="w", width=140).pack(side="left")
        entry = ctk.CTkEntry(frame, width=200)
        entry.pack(side="left", fill="x", expand=True)
        return entry
    
    def create_combo(self, parent, label, values):
        """Create labeled combobox"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame, text=label, anchor="w", width=140).pack(side="left")
        combo = ctk.CTkComboBox(frame, values=values, width=200)
        combo.set(values[0])
        combo.pack(side="left")
        return combo
    
    def add_block(self):
        """Add a new block based on selected type"""
        block_type = self.block_type_combo.get()
        
        block_frame = ctk.CTkFrame(self.blocks_frame, fg_color="#2b2b2b", 
                                  corner_radius=10, border_width=2, border_color="#3498db")
        block_frame.pack(fill="x", padx=5, pady=5)
        
        # Block header
        header = ctk.CTkFrame(block_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=5)
        
        # Block type indicator with color
        color = self.get_block_color(block_type)
        ctk.CTkLabel(header, text=f"🔷 {block_type}", font=("Arial", 12, "bold"),
                    text_color=color).pack(side="left")
        
        # Delete button
        delete_btn = ctk.CTkButton(header, text="🗑️", width=30, height=30,
                                  fg_color="#e74c3c", hover_color="#c0392b",
                                  command=lambda: self.delete_block(block_frame))
        delete_btn.pack(side="right")
        
        # Move buttons
        up_btn = ctk.CTkButton(header, text="↑", width=30, height=30,
                              command=lambda: self.move_block(block_frame, -1))
        up_btn.pack(side="right", padx=2)
        
        down_btn = ctk.CTkButton(header, text="↓", width=30, height=30,
                                command=lambda: self.move_block(block_frame, 1))
        down_btn.pack(side="right", padx=2)
        
        # Block content based on type
        content = ctk.CTkFrame(block_frame, fg_color="transparent")
        content.pack(fill="x", padx=10, pady=5)
        
        block_data = {'type': block_type, 'widgets': {}}
        
        if block_type == "REQUEST":
            self.create_request_block(content, block_data)
        elif block_type == "PARSE":
            self.create_parse_block(content, block_data)
        elif block_type == "KEYCHECK":
            self.create_keycheck_block(content, block_data)
        elif block_type == "FUNCTION":
            self.create_function_block(content, block_data)
        elif block_type == "UTILITY":
            self.create_utility_block(content, block_data)
        elif block_type == "CAPTCHA":
            self.create_captcha_block(content, block_data)
        elif block_type == "TCP":
            self.create_tcp_block(content, block_data)
        elif block_type == "BYPASS_CF":
            self.create_bypass_cf_block(content, block_data)
        elif block_type == "BROWSER_ACTION":
            self.create_browser_action_block(content, block_data)
        elif block_type == "ELEMENT_ACTION":
            self.create_element_action_block(content, block_data)
        elif block_type == "EXECUTE_JS":
            self.create_execute_js_block(content, block_data)
        elif block_type == "NAVIGATE":
            self.create_navigate_block(content, block_data)
        
        self.block_widgets.append((block_frame, block_data))
    
    def get_block_color(self, block_type):
        """Get color for block type"""
        colors = {
            "REQUEST": "#2ecc71", "PARSE": "#f39c12", "KEYCHECK": "#3498db",
            "FUNCTION": "#9b59b6", "UTILITY": "#e74c3c", "CAPTCHA": "#e67e22",
            "TCP": "#95a5a6", "BYPASS_CF": "#e74c3c", "BROWSER_ACTION": "#1abc9c",
            "ELEMENT_ACTION": "#f1c40f", "EXECUTE_JS": "#9b59b6", "NAVIGATE": "#16a085"
        }
        return colors.get(block_type, "#ffffff")
    
    def create_request_block(self, parent, block_data):
        """Create REQUEST block fields"""
        w = block_data['widgets']
        
        w['url'] = self.create_block_entry(parent, "URL:", "https://example.com/api")
        w['method'] = self.create_block_combo(parent, "Method:", ["GET", "POST", "PUT", "DELETE", "PATCH"])
        
        ctk.CTkLabel(parent, text="Headers (JSON):").pack(anchor="w", padx=5)
        w['headers'] = ctk.CTkTextbox(parent, height=60)
        w['headers'].pack(fill="x", padx=5, pady=2)
        w['headers'].insert("1.0", '{"User-Agent": "Mozilla/5.0", "Cookie": "<COOKIES_RAW>"}')
        
        ctk.CTkLabel(parent, text="Body (optional):").pack(anchor="w", padx=5)
        w['body'] = ctk.CTkTextbox(parent, height=40)
        w['body'].pack(fill="x", padx=5, pady=2)
        
        w['save_response'] = self.create_block_entry(parent, "Save Response As:", "response")
    
    def create_parse_block(self, parent, block_data):
        """Create enhanced PARSE block with LR, CSS, XPath, JSON, Regex"""
        w = block_data['widgets']
        
        w['source'] = self.create_block_entry(parent, "Source Variable:", "response")
        w['parse_type'] = self.create_block_combo(parent, "Parse Type:", 
                                                  ["LR", "CSS", "XPath", "JSON", "Regex"])
        
        # Type-specific fields
        w['left'] = self.create_block_entry(parent, "Left String (LR):", "")
        w['right'] = self.create_block_entry(parent, "Right String (LR):", "")
        w['selector'] = self.create_block_entry(parent, "Selector (CSS/XPath):", "")
        w['json_path'] = self.create_block_entry(parent, "JSON Path:", "$.data.field")
        w['pattern'] = self.create_block_entry(parent, "Regex Pattern:", r"(\d+)")
        
        w['capture_name'] = self.create_block_entry(parent, "Capture Variable Name:", "captured")
        w['recursive'] = self.create_block_checkbox(parent, "Recursive (capture all)")
        w['case_sensitive'] = self.create_block_checkbox(parent, "Case Sensitive")
    
    def create_keycheck_block(self, parent, block_data):
        """Create enhanced KEYCHECK block with advanced comparers"""
        w = block_data['widgets']
        
        ctk.CTkLabel(parent, text="Conditions:", font=("Arial", 11, "bold")).pack(anchor="w", padx=5)
        
        # Conditions frame
        cond_frame = ctk.CTkFrame(parent)
        cond_frame.pack(fill="x", padx=5, pady=5)
        
        w['left'] = self.create_block_entry(cond_frame, "Left:", "<username>")
        w['comparer'] = self.create_block_combo(cond_frame, "Comparer:", 
                                               ["EqualTo", "NotEqualTo", "Contains", "NotContains",
                                                "StartsWith", "EndsWith", "GreaterThan", "LessThan",
                                                "MatchesRegex", "Exists", "DoesNotExist"])
        w['right'] = self.create_block_entry(cond_frame, "Right:", "")
        
        w['logic'] = self.create_block_combo(parent, "Logic:", ["AND", "OR"])
        w['success'] = self.create_block_combo(parent, "On Success:", ["HIT", "CUSTOM", "BAN"])
        w['failure'] = self.create_block_combo(parent, "On Failure:", ["BAD", "RETRY", "BAN"])
    
    def create_function_block(self, parent, block_data):
        """Create enhanced FUNCTION block with 30+ functions"""
        w = block_data['widgets']
        
        functions = [
            "Hash-MD5", "Hash-SHA1", "Hash-SHA256", "Hash-SHA384", "Hash-SHA512",
            "HMAC", "Base64-Encode", "Base64-Decode", "URLEncode", "URLDecode",
            "HTMLEntityEncode", "HTMLEntityDecode", "UnixTimeToDate", "DateToUnixTime",
            "CurrentUnixTime", "Replace", "Substring", "CharAt", "CountOccurrences",
            "RandomNum", "RandomString", "Length", "Uppercase", "Lowercase",
            "Reverse", "Trim", "Split", "Join", "Translate"
        ]
        
        w['function'] = self.create_block_combo(parent, "Function:", functions)
        w['input'] = self.create_block_entry(parent, "Input:", "<variable>")
        w['param1'] = self.create_block_entry(parent, "Parameter 1:", "")
        w['param2'] = self.create_block_entry(parent, "Parameter 2:", "")
        w['save_as'] = self.create_block_entry(parent, "Save Result As:", "result")
    
    def create_utility_block(self, parent, block_data):
        """Create UTILITY block with list ops, file ops, delays"""
        w = block_data['widgets']
        
        utilities = [
            "List-Create", "List-Length", "List-Join", "List-Sort", "List-Add",
            "List-Remove", "List-RemoveDuplicates", "List-Random", "List-Shuffle",
            "Variable-Set", "Variable-Split", "File-Exists", "File-Read", "File-Write",
            "File-Append", "File-Delete", "Folder-Exists", "Folder-Create", "Delay"
        ]
        
        w['utility'] = self.create_block_combo(parent, "Utility:", utilities)
        w['input'] = self.create_block_entry(parent, "Input/Path:", "")
        w['value'] = self.create_block_entry(parent, "Value:", "")
        w['save_as'] = self.create_block_entry(parent, "Save As:", "result")
    
    def create_captcha_block(self, parent, block_data):
        """Create CAPTCHA block"""
        w = block_data['widgets']
        
        w['service'] = self.create_block_combo(parent, "CAPTCHA Service:", 
                                              ["2Captcha", "AntiCaptcha", "DeathByCaptcha", "ImageTyperz"])
        w['api_key'] = self.create_block_entry(parent, "API Key:", "")
        w['site_key'] = self.create_block_entry(parent, "Site Key:", "")
        w['page_url'] = self.create_block_entry(parent, "Page URL:", "")
        w['captcha_type'] = self.create_block_combo(parent, "Type:", ["reCAPTCHA v2", "reCAPTCHA v3", "hCaptcha"])
        w['save_as'] = self.create_block_entry(parent, "Save Token As:", "captcha_token")
    
    def create_tcp_block(self, parent, block_data):
        """Create TCP block"""
        w = block_data['widgets']
        
        w['host'] = self.create_block_entry(parent, "Host:", "example.com")
        w['port'] = self.create_block_entry(parent, "Port:", "80")
        w['send_data'] = self.create_block_entry(parent, "Send Data:", "")
        w['timeout'] = self.create_block_entry(parent, "Timeout (s):", "10")
        w['ssl'] = self.create_block_checkbox(parent, "Use SSL/TLS")
        w['save_as'] = self.create_block_entry(parent, "Save Response As:", "tcp_response")
    
    def create_bypass_cf_block(self, parent, block_data):
        """Create Cloudflare bypass block"""
        w = block_data['widgets']
        
        w['url'] = self.create_block_entry(parent, "URL:", "https://example.com")
        w['user_agent'] = self.create_block_entry(parent, "User-Agent:", "Mozilla/5.0...")
        w['timeout'] = self.create_block_entry(parent, "Timeout (s):", "30")
        w['save_cookies'] = self.create_block_checkbox(parent, "Save CF Cookies")
    
    def create_browser_action_block(self, parent, block_data):
        """Create BROWSER ACTION block for Selenium/Playwright"""
        w = block_data['widgets']
        
        actions = ["Click", "Type", "Wait", "Screenshot", "ExecuteJS", "Scroll", 
                  "SwitchTab", "SwitchIframe", "CloseTab"]
        
        w['action'] = self.create_block_combo(parent, "Action:", actions)
        w['selector'] = self.create_block_entry(parent, "Selector:", "#element-id")
        w['by'] = self.create_block_combo(parent, "By:", ["CSS", "XPath", "ID", "Class"])
        w['value'] = self.create_block_entry(parent, "Value/Text:", "")
        w['timeout'] = self.create_block_entry(parent, "Timeout (s):", "10")
    
    def create_element_action_block(self, parent, block_data):
        """Create ELEMENT ACTION block"""
        w = block_data['widgets']
        
        w['selector'] = self.create_block_entry(parent, "Selector:", "#element")
        w['by'] = self.create_block_combo(parent, "Find By:", ["CSS", "XPath", "ID", "Class", "Name"])
        w['action'] = self.create_block_combo(parent, "Action:", 
                                             ["GetText", "GetAttribute", "GetHTML", "CheckExists", "CheckVisible"])
        w['attribute'] = self.create_block_entry(parent, "Attribute Name:", "href")
        w['save_as'] = self.create_block_entry(parent, "Save As:", "element_data")
    
    def create_execute_js_block(self, parent, block_data):
        """Create EXECUTE JS block"""
        w = block_data['widgets']
        
        ctk.CTkLabel(parent, text="JavaScript Code:").pack(anchor="w", padx=5)
        w['script'] = ctk.CTkTextbox(parent, height=80)
        w['script'].pack(fill="x", padx=5, pady=2)
        w['script'].insert("1.0", "return document.title;")
        
        w['save_as'] = self.create_block_entry(parent, "Save Result As:", "js_result")
    
    def create_navigate_block(self, parent, block_data):
        """Create NAVIGATE block"""
        w = block_data['widgets']
        
        w['action'] = self.create_block_combo(parent, "Action:", 
                                             ["NavigateTo", "GoBack", "GoForward", "Refresh", "WaitForLoad"])
        w['url'] = self.create_block_entry(parent, "URL:", "https://example.com")
        w['timeout'] = self.create_block_entry(parent, "Timeout (s):", "10")
    
    def create_block_entry(self, parent, label, default=""):
        """Create entry in block"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(frame, text=label, width=150, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", fill="x", expand=True)
        if default:
            entry.insert(0, default)
        return entry
    
    def create_block_combo(self, parent, label, values):
        """Create combobox in block"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=5, pady=2)
        
        ctk.CTkLabel(frame, text=label, width=150, anchor="w").pack(side="left")
        combo = ctk.CTkComboBox(frame, values=values, width=300)
        combo.set(values[0])
        combo.pack(side="left")
        return combo
    
    def create_block_checkbox(self, parent, label):
        """Create checkbox in block"""
        var = ctk.BooleanVar()
        check = ctk.CTkCheckBox(parent, text=label, variable=var)
        check.pack(anchor="w", padx=5, pady=2)
        return var
    
    def delete_block(self, block_frame):
        """Delete a block"""
        for i, (frame, data) in enumerate(self.block_widgets):
            if frame == block_frame:
                self.block_widgets.pop(i)
                break
        block_frame.destroy()
    
    def move_block(self, block_frame, direction):
        """Move block up or down"""
        for i, (frame, data) in enumerate(self.block_widgets):
            if frame == block_frame:
                new_index = i + direction
                if 0 <= new_index < len(self.block_widgets):
                    # Swap in list
                    self.block_widgets[i], self.block_widgets[new_index] = \
                        self.block_widgets[new_index], self.block_widgets[i]
                    
                    # Re-pack frames
                    for f, _ in self.block_widgets:
                        f.pack_forget()
                    for f, _ in self.block_widgets:
                        f.pack(fill="x", padx=5, pady=5)
                break
    
    def collect_config_data(self):
        """Collect all config data from UI"""
        self.config_data['name'] = self.name_entry.get()
        self.config_data['author'] = self.author_entry.get()
        self.config_data['version'] = self.version_entry.get()
        self.config_data['url'] = self.url_entry.get()
        self.config_data['method'] = self.method_combo.get()
        self.config_data['cookie_format'] = self.cookie_format_combo.get()
        self.config_data['needs_stealth'] = self.stealth_var.get()
        self.config_data['use_selenium'] = self.selenium_var.get()
        self.config_data['browser_mode'] = self.browser_mode_combo.get()
        self.config_data['timeout'] = int(self.timeout_entry.get() or 15)
        
        # Collect blocks
        blocks = []
        for _, block_data in self.block_widgets:
            block = {'type': block_data['type']}
            widgets = block_data['widgets']
            
            # Extract widget values based on type
            for key, widget in widgets.items():
                if isinstance(widget, ctk.CTkEntry):
                    block[key] = widget.get()
                elif isinstance(widget, ctk.CTkComboBox):
                    block[key] = widget.get()
                elif isinstance(widget, ctk.BooleanVar):
                    block[key] = widget.get()
                elif isinstance(widget, ctk.CTkTextbox):
                    block[key] = widget.get("1.0", "end-1c")
            
            blocks.append(block)
        
        self.config_data['blocks'] = blocks
        return self.config_data
    
    def save_config(self):
        """Save config to JSON file"""
        config = self.collect_config_data()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="../configs"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
                messagebox.showinfo("Success", f"Config saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save config: {e}")
    
    def load_config(self):
        """Load config from JSON file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir="../configs"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                
                # Load config info
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, config.get('name', ''))
                
                self.author_entry.delete(0, "end")
                self.author_entry.insert(0, config.get('author', ''))
                
                self.version_entry.delete(0, "end")
                self.version_entry.insert(0, config.get('version', ''))
                
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, config.get('url', ''))
                
                self.method_combo.set(config.get('method', 'GET'))
                self.cookie_format_combo.set(config.get('cookie_format', 'netscape'))
                self.stealth_var.set(config.get('needs_stealth', False))
                self.selenium_var.set(config.get('use_selenium', False))
                self.browser_mode_combo.set(config.get('browser_mode', 'headless'))
                
                self.timeout_entry.delete(0, "end")
                self.timeout_entry.insert(0, str(config.get('timeout', 15)))
                
                # Clear existing blocks
                for frame, _ in self.block_widgets:
                    frame.destroy()
                self.block_widgets.clear()
                
                # Load blocks (simplified - would need full implementation)
                messagebox.showinfo("Loaded", f"Config loaded from {file_path}\n\nNote: Block loading is partially implemented")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")
    
    def preview_json(self):
        """Preview config as JSON"""
        config = self.collect_config_data()
        
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("📝 JSON Preview")
        preview_window.geometry("600x700")
        
        ctk.CTkLabel(preview_window, text="Config JSON Preview", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        text_frame = ctk.CTkFrame(preview_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text = ctk.CTkTextbox(text_frame, wrap="word")
        text.pack(fill="both", expand=True)
        
        json_str = json.dumps(config, indent=2)
        text.insert("1.0", json_str)
        text.configure(state="disabled")
        
        ctk.CTkButton(preview_window, text="Close", command=preview_window.destroy,
                     width=100).pack(pady=10)
