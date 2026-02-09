import customtkinter as ctk
import threading
from core import JokerSigmaCore

class JokerSigmaTerminal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JOKER // SIGMA FRAMEWORK V99")
        self.geometry("1400x900")
        ctk.set_appearance_mode("dark")
        
        self.core = JokerSigmaCore()
        self.intel_cache = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        self.sidebar = ctk.CTkFrame(self, width=320, fg_color="#000", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="JOKER", font=("Impact", 70), text_color="#FF0000").pack(pady=(60, 0))
        ctk.CTkLabel(self.sidebar, text="SIGMA EDITION", font=("Courier", 16, "bold"), text_color="#FFF").pack()
        
        self.status_pnl = ctk.CTkFrame(self.sidebar, fg_color="#050505", border_width=1, border_color="#1a1a1a")
        self.status_pnl.pack(fill="x", padx=25, pady=60)
        self.status_txt = ctk.CTkLabel(self.status_pnl, text="● READY", text_color="#00FF00", font=("Courier", 18, "bold"))
        self.status_txt.pack(pady=25)

        
        self.hub = ctk.CTkFrame(self, fg_color="#080808", corner_radius=25)
        self.hub.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")

        self.nav = ctk.CTkFrame(self.hub, fg_color="transparent")
        self.nav.pack(fill="x", padx=45, pady=45)

        self.target_box = ctk.CTkEntry(self.nav, placeholder_text="SCAN VECTOR (IP/DOMAIN)", width=700, height=65, font=("Courier", 20), border_color="#111", fg_color="#000")
        self.target_box.pack(side="left", padx=(0, 20))

        self.fire_btn = ctk.CTkButton(self.nav, text="EXECUTE", fg_color="#FF0000", text_color="#FFF", font=("Courier", 20, "bold"), width=180, height=65, hover_color="#8B0000", command=self.fire)
        self.fire_btn.pack(side="left")

        self.terminal = ctk.CTkTextbox(self.hub, fg_color="#000", text_color="#00FF00", font=("Courier New", 16), border_width=1, border_color="#111")
        self.terminal.pack(fill="both", expand=True, padx=45, pady=(0, 45))

        self.export_btn = ctk.CTkButton(self.hub, text="EXPORT SIGMA PDF REPORT", fg_color="transparent", border_width=2, border_color="#FF0000", text_color="#FF0000", font=("Courier", 16, "bold"), state="disabled", height=55, command=self.export)
        self.export_btn.pack(pady=(0, 45))

    def log(self, text):
        self.terminal.insert("end", f"[Σ-JOKER]> {text}\n")
        self.terminal.see("end")

    def fire(self):
        target = self.target_box.get()
        if not target: return
        self.terminal.delete("1.0", "end")
        self.status_txt.configure(text="● ACTIVE", text_color="#FF0000")
        self.export_btn.configure(state="disabled")
        threading.Thread(target=self._mission, args=(target,), daemon=True).start()

    def _mission(self, target):
        try:
            self.log(f"LAUNCHING SIGMA PROTOCOL ON {target}...")
            self.intel_cache = self.core.execute_elite_audit(target)
            
            for node in self.intel_cache['nodes']:
                self.log(f"HOST ACQUIRED: {node['address']} | OS: {node['os']}")
                for v in node['vectors']:
                    self.log(f"  [+] PORT {v['port']} // {v['service']} // {v['product']}")
            
            self.status_txt.configure(text="● COMPLETE", text_color="#00FF00")
            self.export_btn.configure(state="normal")
            self.log("MISSION ACCOMPLISHED. SYSTEM STABILIZED.")
        except Exception as e:
            self.log(f"CRITICAL ERROR: {e}")
            self.status_txt.configure(text="● FAILURE", text_color="red")

    def export(self):
        if self.intel_cache:
            p = self.core.build_sigma_report(self.intel_cache)
            self.log(f"SIGMA INTEL REPORT SAVED: {p}")

if __name__ == "__main__":
    app = JokerSigmaTerminal()
    app.mainloop()
