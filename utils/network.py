import requests
from typing import Optional
import logging

# Configura logger para este módulo
logger = logging.getLogger(__name__)

def fetch_html(url: str) -> Optional[str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'es-ES,es;q=0.9'
    }
    try:
        logger.info(f"Conectando a: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.text
    except requests.RequestException as e:
        logger.error(f"Error al obtener la página: {str(e)}")
        return None
    