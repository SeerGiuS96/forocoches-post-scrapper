import sys
import logging
from bs4 import BeautifulSoup
from src.scraper import ForoCochesScraper
from utils.network import fetch_html
from utils.file_handler import save_posts_to_json

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

THREAD_ID = "10343939"  # <-- Pon aquí el ID del hilo que quieras scrapear

def get_thread_url(thread_id, page=1):
    """Devuelve la URL del hilo a partir del ID y la página"""
    base_url = "https://www.forocoches.com/foro/"
    if page == 1:
        return f"{base_url}showthread.php?t={thread_id}"
    else:
        return f"{base_url}showthread.php?t={thread_id}&page={page}"

def get_last_page(html):
    soup = BeautifulSoup(html, "html.parser")
    # Busca el paginador desktop
    pagenav = soup.find("div", class_="pagenav-desktop")
    if not pagenav:
        return 1  # Solo una página
    # Busca todos los <a> y <span> que puedan tener el número de página
    page_numbers = []
    for tag in pagenav.find_all(["a", "span"]):
        try:
            num = int(tag.get_text(strip=True))
            page_numbers.append(num)
        except ValueError:
            continue
    return max(page_numbers) if page_numbers else 1

def main():
    try:
        logger.info("Iniciando scraper...")
        scraper = ForoCochesScraper()
        all_posts = []

        # 1. Descarga la primera página y detecta el total de páginas
        page = 1
        url = get_thread_url(THREAD_ID, page)
        logger.info(f"URL: {url}")
        html = fetch_html(url)
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html if html else "")
        if not html:
            logger.error(f"No se pudo obtener el HTML de la página {page}")
            return

        last_page = get_last_page(html)
        logger.info(f"El hilo tiene {last_page} páginas.")

        # 2. Procesa todas las páginas
        for page in range(1, last_page + 1):
            url = get_thread_url(THREAD_ID, page)
            logger.info(f"URL: {url}")
            html = fetch_html(url)
            if not html:
                logger.error(f"No se pudo obtener el HTML de la página {page}")
                break

            posts = scraper.scrape_thread(html)
            if not posts:
                logger.info(f"No se encontraron posts en la página {page}.")
                continue

            logger.info(f"Encontrados {len(posts)} posts en la página {page}")
            all_posts.extend(posts)

        if all_posts:
            logger.info(f"Total de posts encontrados: {len(all_posts)}")
            save_posts_to_json(all_posts, 'forocoches_posts.json')
            logger.info("Datos guardados correctamente")
        else:
            logger.warning("No se encontraron posts en el hilo.")

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    main()