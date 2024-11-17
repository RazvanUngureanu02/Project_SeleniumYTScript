import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # Nivelul minim de loguri
        format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
        handlers=[
            logging.FileHandler("application.log"),  # Logg-urile merg într-un singur fișier
            logging.StreamHandler()  # Opțional: afișare în consolă
        ]
    )
    return logging.getLogger("AppLogger")
