import json
import logging
from typing import List
from src.models import Post

logger = logging.getLogger(__name__)

def save_posts_to_json(posts, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error al guardar archivo: {str(e)}")