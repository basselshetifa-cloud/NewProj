import customtkinter as ctk
import json

class ConfigEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OpenBullet Config Editor")
        self.geometry("800x600")

        # Left panel: Config Info
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.pack(side="left", fill="both")

        self.name_entry = self.create_entry("Name")
        self.url_entry = self.create_entry("URL")
        self.method_entry = self.create_entry("Method")
        self.cookie_format_entry = self.create_entry("Cookie Format")
        self.stealth_mode_var = ctk.CTkCheckBox(self.left_panel, text="Stealth Mode")
        self.proxy_entry = self.create_entry("Proxy")
        self.timeout_entry = self.create_entry("Timeout")

        # Right panel: Scrollable Blocks Area
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.blocks_list = ctk.CTkScrollableFrame(self.right_panel)
        self.blocks_list.pack(fill="both", expand=True)

        self.add_block_button = ctk.CTkButton(self.right_panel, text="Add Block", command=self.add_block)
        self.add_block_button.pack()

        self.save_button = ctk.CTkButton(self.left_panel, text="Save Config", command=self.save_config)
        self.load_button = ctk.CTkButton(self.left_panel, text="Load Config", command=self.load_config)
        self.save_button.pack()
        self.load_button.pack()

        self.blocks = []

    def create_entry(self, label):
        frame = ctk.CTkFrame(self.left_panel)
        frame.pack()
        ctk.CTkLabel(frame, text=label).pack(side="left")
        entry = ctk.CTkEntry(frame)
        entry.pack(side="right")
        return entry

    def add_block(self):
        # Logic to add blocks of various types.
        pass

    def save_config(self):
        config = {
            'name': self.name_entry.get(),
            'url': self.url_entry.get(),
            'method': self.method_entry.get(),
            'cookie_format': self.cookie_format_entry.get(),
            'stealth_mode': self.stealth_mode_var.get(),
            'proxy': self.proxy_entry.get(),
            'timeout': self.timeout_entry.get(),
            'blocks': self.blocks
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)

    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.name_entry.insert(0, config['name'])
            self.url_entry.insert(0, config['url'])
            # Load other fields...


if __name__ == "__main__":
    app = ConfigEditor()
    app.mainloop()