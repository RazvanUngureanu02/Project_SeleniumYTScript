import tkinter as tk
from tkinter import messagebox
import threading

class YouTubeGUI:
    def __init__(self, yt_browser):
        self.yt_browser = yt_browser
        self.video_data = None
        self.duration = None

    def is_url(self, input_text):
        return input_text.startswith("http://") or input_text.startswith("https://")

    def validate_duration(self):
        if not self.duration.get().isdigit():
            return False
        seconds = int(self.duration.get())
        return 1 <= seconds <= 120

    def run_in_thread(self, target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        thread.start()

    def open_url(self):
        input_text = self.video_data.get()
        if not input_text or not self.is_url(input_text):
            messagebox.showerror("Eroare", "Introduceți un URL valid pentru a utiliza Open.")
            return
        if not self.validate_duration():
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        print(f"Deschidem URL-ul: {input_text}")
        self.run_in_thread(self.yt_browser.open_video_url, input_text)

    def search_video(self):
        input_text = self.video_data.get()
        if not input_text or self.is_url(input_text):
            messagebox.showerror("Eroare", "Introduceți un cuvânt sau o expresie pentru a utiliza Search.")
            return
        if not self.validate_duration():
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        print(f"Căutăm videoclipul: {input_text}")
        self.run_in_thread(self.yt_browser.search_and_play, input_text)

    def edit_entry(self):
        self.video_entry.delete(0, tk.END)
        self.video_entry.focus()

    def submit(self):
        input_text = self.video_data.get()
        if not input_text:
            messagebox.showerror("Eroare", "Introduceți un URL sau un nume valid.")
            return
        if not self.validate_duration():
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        self.root.destroy()  # Închidem interfața și începem înregistrarea

    def on_close(self):
        """Funcția apelată când utilizatorul închide fereastra."""
        if messagebox.askokcancel("Ieșire", "Sigur doriți să închideți aplicația?"):
            print("Închidem browser-ul...")
            self.yt_browser.close()  # Închidem browser-ul
            self.root.destroy()  # Închidem interfața grafică

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Control YouTube Video")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        # Eveniment pentru închiderea ferestrei
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.video_data = tk.StringVar()
        self.duration = tk.StringVar()

        tk.Label(self.root, text="Introduceți URL-ul sau numele videoclipului YouTube:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        self.video_entry = tk.Entry(self.root, textvariable=self.video_data, width=40, font=("Arial", 12))
        self.video_entry.pack(pady=5)

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Open", command=self.open_url, bg="#4CAF50", fg="white", font=("Arial", 10), width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_video, bg="#2196F3", fg="white", font=("Arial", 10), width=10).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_entry, bg="#FFC107", fg="black", font=("Arial", 10), width=10).grid(row=0, column=2, padx=5)

        tk.Label(self.root, text="Durata înregistrării (secunde):", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        tk.Entry(self.root, textvariable=self.duration, width=10, font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Submit", command=self.submit, bg="#E91E63", fg="white", font=("Arial", 10)).pack(pady=20)

        self.root.mainloop()

        return self.video_data.get(), int(self.duration.get() if self.validate_duration() else 0)