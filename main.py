import sys
import logging
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

def get_thread_url(thread_id):
    """Devuelve la URL del hilo a partir del ID"""
    base_url = "https://www.forocoches.com/foro/"
    return f"{base_url}showthread.php?t={thread_id}"

def main():
    try:
        logger.info("Iniciando scraper...")
        url = get_thread_url(THREAD_ID)
        logger.info(f"URL: {url}")
        
        html = fetch_html(url)
        # Guarda el HTML descargado para depuración
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html if html else "")
        if not html:
            logger.error("No se pudo obtener el HTML")
            return
            
        scraper = ForoCochesScraper()
        posts = scraper.scrape_thread(html)
        
        if posts:
            logger.info(f"Encontrados {len(posts)} posts")
            save_posts_to_json(posts, 'forocoches_posts.json')
            logger.info("Datos guardados correctamente")
        else:
            logger.warning("No se encontraron posts")
            
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")

if __name__ == '__main__':
    main()