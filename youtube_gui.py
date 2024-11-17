import tkinter as tk
from tkinter import messagebox
import threading
import logging

# Configurăm logging-ul
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("application.log"),  # Log-urile vor fi salvate în application.log
        logging.StreamHandler()  # Log-urile vor fi afișate și în consolă
    ]
)
logger = logging.getLogger("YouTubeGUI")  # Creăm un logger pentru acest script

class YouTubeGUI:
    def __init__(self, yt_browser):
        """
        Inițializează interfața grafică pentru controlul YouTube.
        :param yt_browser: Instanță a clasei YouTubeBrowser pentru a gestiona browser-ul.
        """
        self.yt_browser = yt_browser
        self.video_data = None
        self.duration = None
        logger.info("YouTubeGUI a fost inițializat cu succes.")

    def is_url(self, input_text):
        """
        Verifică dacă textul introdus este un URL valid.
        :param input_text: Textul de verificat.
        :return: True dacă textul este un URL valid, altfel False.
        """
        result = input_text.startswith("http://") or input_text.startswith("https://")
        logger.info(f"Validare URL pentru '{input_text}': {result}")
        return result

    def validate_duration(self):
        """
        Validează dacă durata introdusă este un număr între 1 și 120 secunde.
        :return: True dacă durata este validă, altfel False.
        """
        if not self.duration.get().isdigit():
            logger.warning("Durata introdusă nu este un număr valid.")
            return False
        seconds = int(self.duration.get())
        is_valid = 1 <= seconds <= 120
        logger.info(f"Validare durată: {seconds} secunde. Este validă? {is_valid}")
        return is_valid

    def run_in_thread(self, target, *args):
        """
        Rulează o funcție într-un thread separat.
        :param target: Funcția de executat.
        :param args: Argumentele funcției.
        """
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        thread.start()
        logger.info(f"Thread pornit pentru funcția {target.__name__}")

    def open_url(self):
        """
        Deschide un videoclip pe baza URL-ului introdus de utilizator.
        """
        input_text = self.video_data.get()
        if not input_text or not self.is_url(input_text):
            logger.error("URL invalid introdus pentru Open.")
            messagebox.showerror("Eroare", "Introduceți un URL valid pentru a utiliza Open.")
            return
        if not self.validate_duration():
            logger.error("Durată invalidă introdusă pentru Open.")
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        logger.info(f"Deschidem URL-ul: {input_text}")
        self.run_in_thread(self.yt_browser.open_video_url, input_text)

    def search_video(self):
        """
        Caută un videoclip pe baza textului introdus de utilizator.
        """
        input_text = self.video_data.get()
        if not input_text or self.is_url(input_text):
            logger.error("Input invalid introdus pentru Search.")
            messagebox.showerror("Eroare", "Introduceți un cuvânt sau o expresie pentru a utiliza Search.")
            return
        if not self.validate_duration():
            logger.error("Durată invalidă introdusă pentru Search.")
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        logger.info(f"Căutăm videoclipul: {input_text}")
        self.run_in_thread(self.yt_browser.search_and_play, input_text)

    def edit_entry(self):
        """
        Curăță câmpul de intrare și setează focusul pe acesta.
        """
        logger.info("Editarea câmpului de intrare a fost inițiată.")
        self.video_entry.delete(0, tk.END)
        self.video_entry.focus()

    def submit(self):
        """
        Validează intrările și finalizează interfața grafică.
        """
        input_text = self.video_data.get()
        if not input_text:
            logger.error("Input gol introdus la Submit.")
            messagebox.showerror("Eroare", "Introduceți un URL sau un nume valid.")
            return
        if not self.validate_duration():
            logger.error("Durată invalidă introdusă la Submit.")
            messagebox.showerror("Eroare", "Introduceți o durată validă (1-120 secunde).")
            return
        logger.info("Submit a fost apăsat. Închidem interfața grafică și începem înregistrarea.")
        self.root.destroy()

    def on_close(self):
        """
        Funcția apelată când utilizatorul închide fereastra aplicației.
        """
        if messagebox.askokcancel("Ieșire", "Sigur doriți să închideți aplicația?"):
            logger.info("Utilizatorul a ales să închidă aplicația.")
            try:
                self.yt_browser.close()
                logger.info("Browser-ul a fost închis cu succes.")
            except Exception as e:
                logger.error(f"Eroare la închiderea browser-ului: {e}")
            self.root.destroy()

    def create_gui(self):
        """
        Creează interfața grafică a aplicației.
        """
        self.root = tk.Tk()
        self.root.title("Control YouTube Video")
        self.root.geometry("400x300")  # Setăm dimensiunea ferestrei
        self.root.configure(bg="#f0f0f0")  # Setăm culoarea de fundal

        # Gestionăm evenimentul de închidere a ferestrei
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Variabilele pentru stocarea datelor de intrare
        self.video_data = tk.StringVar()
        self.duration = tk.StringVar()

        # Etichetă și câmp de intrare pentru URL/numele videoclipului
        tk.Label(self.root, text="Introduceți URL-ul sau numele videoclipului YouTube:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        self.video_entry = tk.Entry(self.root, textvariable=self.video_data, width=40, font=("Arial", 12))
        self.video_entry.pack(pady=5)

        # Cadru pentru butoane
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Butoanele Open, Search, Edit
        tk.Button(button_frame, text="Open", command=self.open_url, bg="#4CAF50", fg="white", font=("Arial", 10), width=10).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_video, bg="#2196F3", fg="white", font=("Arial", 10), width=10).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_entry, bg="#FFC107", fg="black", font=("Arial", 10), width=10).grid(row=0, column=2, padx=5)

        # Etichetă și câmp de intrare pentru durata înregistrării
        tk.Label(self.root, text="Durata înregistrării (secunde):", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        tk.Entry(self.root, textvariable=self.duration, width=10, font=("Arial", 12)).pack(pady=5)

        # Butonul Submit
        tk.Button(self.root, text="Submit", command=self.submit, bg="#E91E63", fg="white", font=("Arial", 10)).pack(pady=20)

        logger.info("Interfața grafică a fost creată.")

        self.root.mainloop()

        return self.video_data.get(), int(self.duration.get() if self.validate_duration() else 0)
