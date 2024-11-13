import tkinter as tk
from tkinter import messagebox
import threading

def create_gui(yt_browser):
    def is_url(input_text):
        return input_text.startswith("http://") or input_text.startswith("https://")

    def run_in_thread(target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        thread.start()

    def open_url():
        input_text = video_data.get()
        if not input_text or not is_url(input_text):
            messagebox.showerror("Eroare", "Introduceți un URL valid pentru a utiliza Open.")
            return
        print(f"Deschidem URL-ul: {input_text}")
        run_in_thread(yt_browser.open_video_url, input_text)

    def search_video():
        input_text = video_data.get()
        if not input_text or is_url(input_text):
            messagebox.showerror("Eroare", "Introduceți un cuvânt sau o expresie pentru a utiliza Search.")
            return
        print(f"Căutăm videoclipul: {input_text}")
        run_in_thread(yt_browser.search_and_play, input_text)

    def edit_entry():
        video_entry.delete(0, tk.END)
        video_entry.focus()

    def submit():
        input_text = video_data.get()
        if not duration.get().isdigit() or int(duration.get()) <= 0:
            messagebox.showerror("Eroare", "Introduceți o durată numerică validă.")
            return
        root.destroy()  # Închidem interfața și începem înregistrarea

    root = tk.Tk()
    root.title("Control YouTube Video")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    video_data = tk.StringVar()
    duration = tk.StringVar()

    tk.Label(root, text="Introduceți URL-ul sau numele videoclipului YouTube:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    video_entry = tk.Entry(root, textvariable=video_data, width=40, font=("Arial", 12))
    video_entry.pack(pady=5)

    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Open", command=open_url, bg="#4CAF50", fg="white", font=("Arial", 10), width=10).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Search", command=search_video, bg="#2196F3", fg="white", font=("Arial", 10), width=10).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Edit", command=edit_entry, bg="#FFC107", fg="black", font=("Arial", 10), width=10).grid(row=0, column=2, padx=5)

    tk.Label(root, text="Durata înregistrării (secunde):", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    tk.Entry(root, textvariable=duration, width=10, font=("Arial", 12)).pack(pady=5)

    tk.Button(root, text="Submit", command=submit, bg="#E91E63", fg="white", font=("Arial", 10)).pack(pady=20)

    root.mainloop()

    return video_data.get(), int(duration.get() if duration.get().isdigit() else 0)
