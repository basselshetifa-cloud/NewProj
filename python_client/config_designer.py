"""
Professional Config Designer - LoliScript Editor
Text-based format like OpenBullet
"""
import customtkinter as ctk
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ConfigDesigner(ctk.CTkToplevel):
    """Professional config designer window"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("⚙️ Config Designer")
        self.geometry("1400x900")
        
        self.configs_folder = "configs"
        os.makedirs(self.configs_folder, exist_ok=True)
        
        self.setup_ui()
        self.refresh_configs()
        self.auto_refresh_loop()
    
    def setup_ui(self):
        """Setup professional UI"""
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, height=70, fg_color="#1a1a1a")
        toolbar.pack(fill="x", padx=10, pady=10)
        toolbar.pack_propagate(False)
        
        ctk.CTkLabel(
            toolbar,
            text="⚙️ Config Designer",
            font=("Arial", 22, "bold")
        ).pack(side="left", padx=20)
        
        # Buttons
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(side="left", padx=20)
        
        ctk.CTkButton(
            btn_frame,
            text="📂 New",
            command=self.new_config,
            width=100,
            fg_color="#27ae60"
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Save",
            command=self.save_config,
            width=100,
            fg_color="#3498db"
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Refresh",
            command=self.refresh_configs,
            width=100
        ).pack(side="left", padx=3)
        
        # Main content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # LEFT: Config list
        left = ctk.CTkFrame(content, width=280)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        
        ctk.CTkLabel(
            left,
            text="📁 Configs",
            font=("Arial", 16, "bold")
        ).pack(pady=15)
        
        self.config_list = ctk.CTkScrollableFrame(left)
        self.config_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CENTER: Editor
        center = ctk.CTkFrame(content)
        center.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Name
        name_frame = ctk.CTkFrame(center, fg_color="transparent")
        name_frame.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(name_frame, text="Name:", font=("Arial", 13, "bold")).pack(side="left")
        self.name_entry = ctk.CTkEntry(name_frame, width=350, height=35)
        self.name_entry.pack(side="left", padx=10)
        
        ctk.CTkLabel(center, text="📝 LoliScript Editor", font=("Arial", 16, "bold")).pack()
        
        # Code editor
        editor_frame = ctk.CTkFrame(center)
        editor_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.code_editor = ctk.CTkTextbox(
            editor_frame,
            font=("Consolas", 11),
            wrap="none"
        )
        self.code_editor.pack(fill="both", expand=True)
        
        # RIGHT: Blocks
        right = ctk.CTkFrame(content, width=320)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)
        
        ctk.CTkLabel(right, text="🧩 Blocks", font=("Arial", 16, "bold")).pack(pady=15)
        
        blocks_scroll = ctk.CTkScrollableFrame(right)
        blocks_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        blocks = [
            ("🟢 REQUEST", self.add_request),
            ("🟡 PARSE", self.add_parse),
            ("🔵 KEYCHECK", self.add_keycheck),
            ("🟣 FUNCTION", self.add_function),
            ("🟤 UTILITY", self.add_utility),
            ("🔴 NAVIGATE", self.add_navigate),
            ("🟠 BROWSER", self.add_browser),
        ]
        
        for name, cmd in blocks:
            ctk.CTkButton(
                blocks_scroll,
                text=name,
                command=cmd,
                width=280,
                height=45,
                font=("Arial", 12, "bold"),
                anchor="w"
            ).pack(pady=5)
    
    def new_config(self):
        self.name_entry.delete(0, "end")
        self.code_editor.delete("1.0", "end")
        template = """# Config Template

REQUEST GET "https://example.com"
  HEADER "User-Agent: Mozilla/5.0"
  HEADER "Accept: */*"

KEYCHECK
  KEYCHAIN Success OR
    KEY "success"
  KEYCHAIN Failure OR
    KEY "error"
"""
        self.code_editor.insert("1.0", template)
    
    def save_config(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter config name!")
            return
        
        name = name.replace('.loli', '')
        code = self.code_editor.get("1.0", "end-1c")
        
        filepath = os.path.join(self.configs_folder, f"{name}.loli")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("✅ Saved", f"Saved: {filepath}")
            self.refresh_configs()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_config(self, filename):
        filepath = os.path.join(self.configs_folder, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            name = filename.replace('.loli', '').replace('.json', '')
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, name)
            
            self.code_editor.delete("1.0", "end")
            self.code_editor.insert("1.0", code)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_configs(self):
        for widget in self.config_list.winfo_children():
            widget.destroy()
        
        try:
            files = [f for f in os.listdir(self.configs_folder)
                    if f.endswith(('.loli', '.json'))]
            files.sort()
            
            if files:
                for f in files:
                    ctk.CTkButton(
                        self.config_list,
                        text=f,
                        command=lambda x=f: self.load_config(x),
                        width=240,
                        anchor="w"
                    ).pack(pady=2)
            else:
                ctk.CTkLabel(self.config_list, text="No configs", text_color="gray").pack(pady=20)
        except:
            pass
    
    def auto_refresh_loop(self):
        self.refresh_configs()
        self.after(2000, self.auto_refresh_loop)
    
    def add_request(self):
        self.code_editor.insert("insert", '\nREQUEST GET "https://example.com"\n  HEADER "User-Agent: Mozilla/5.0"\n\n')
    
    def add_parse(self):
        self.code_editor.insert("insert", '\nPARSE "<SOURCE>" LR "left" "right" -> CAP "var"\n\n')
    
    def add_keycheck(self):
        self.code_editor.insert("insert", '\nKEYCHECK\n  KEYCHAIN Success OR\n    KEY "success"\n\n')
    
    def add_function(self):
        self.code_editor.insert("insert", '\nFUNCTION Delay "1000"\n\n')
    
    def add_utility(self):
        self.code_editor.insert("insert", '\nUTILITY Join "list" -> VAR "result"\n\n')
    
    def add_navigate(self):
        self.code_editor.insert("insert", '\nNAVIGATE "https://example.com"\n\n')
    
    def add_browser(self):
        self.code_editor.insert("insert", '\nBROWSERACTION Open\n\n')
