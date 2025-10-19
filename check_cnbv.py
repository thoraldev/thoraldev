import requests
from bs4 import BeautifulSoup

URL = "https://www.gob.mx/cnbv/es/archivo/prensa"
MEMORY_FILE = "last_headline.txt"

def get_latest_headline():
    """Visita la página de la CNBV y extrae el titular y el enlace del comunicado más reciente."""
    try:
        # AÑADIMOS ESTE ENCABEZADO PARA SIMULAR UN NAVEGADOR
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # AÑADIMOS 'headers=headers' A LA PETICIÓN
        page = requests.get(URL, headers=headers)
        
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        
        latest_article = soup.find("div", class_="col-md-8")
        if latest_article:
            headline_element = latest_article.find("h2").find("a")
            if headline_element:
                headline = headline_element.text.strip()
                link = f"https://www.gob.mx{headline_element['href']}"
                return headline, link
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la página: {e}")
    return None, None

def get_last_seen_headline():
    """Lee el último titular guardado."""
    try:
        with open(MEMORY_FILE, "r", encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_new_data(headline, link):
    """Guarda el nuevo titular y el enlace en el archivo de memoria, separados por una línea."""
    with open(MEMORY_FILE, "w", encoding='utf-8') as f:
        f.write(f"{headline}\n{link}")

# --- Flujo principal ---
if __name__ == "__main__":
    print("Iniciando revisión de la CNBV...")
    latest_headline, latest_link = get_latest_headline()
    last_seen = get_last_seen_headline().split('\n')[0]

    if latest_headline and latest_headline != last_seen:
        print(f"¡Nuevo titular encontrado!: {latest_headline}")
        print(f"Enlace: {latest_link}")
        save_new_data(latest_headline, latest_link)
    elif not latest_headline:
        print("No se pudo obtener el titular más reciente.")
    else:
        print("No hay nuevas actualizaciones.")
