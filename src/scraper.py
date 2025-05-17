import re
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def extract_quotes_and_text(message):
    """
    Extrae citas y texto propio de un mensaje.
    Devuelve (texto_propio, lista_de_citas)
    """
    lines = message.split('\n')
    quotes = []
    text_parts = []
    i = 0
    while i < len(lines):
        if lines[i].strip().lower().startswith("cita de"):
            quoted_user = lines[i+1] if i+1 < len(lines) else ""
            quoted_text = ""
            j = i+2
            while j < len(lines) and lines[j].strip():
                quoted_text += lines[j] + "\n"
                j += 1
            quotes.append({
                "quoted_user": quoted_user,
                "quoted_text": quoted_text.strip()
                # Si puedes, añade aquí "quoted_post_id": ...
            })
            i = j
        else:
            text_parts.append(lines[i])
            i += 1
    message_text = "\n".join([t for t in text_parts if t.strip()])
    return message_text, quotes

def extract_mentions(message):
    # Busca menciones tipo @usuario
    return re.findall(r'@(\w+)', message)

def find_quoted_post_id(quotes, posts_so_far):
    for quote in quotes:
        quoted_user = quote["quoted_user"]
        quoted_text = quote["quoted_text"].strip()
        quoted_post_id = None
        # Busca el primer mensaje anterior del usuario citado con texto igual o muy parecido
        for prev in reversed(posts_so_far):
            if prev["username"] == quoted_user and quoted_text and quoted_text in prev["message"]:
                quoted_post_id = prev["post_id"]
                break
        quote["quoted_post_id"] = quoted_post_id

class ForoCochesScraper:
    def scrape_thread(self, html, posts_so_far=None):
        logger.info("Extrayendo posts...")
        soup = BeautifulSoup(html, "html.parser")
        posts_div = soup.find("div", id="posts")
        if not posts_div:
            logger.warning("No se encontró el contenedor de posts")
            return []

        posts = []
        for post_div in posts_div.find_all("div", id=lambda x: x and x.startswith("edit")):
            post_id = post_div.get("id")[4:]  # Quita 'edit' del id para obtener el id numérico

            # Nombre de usuario
            user_elem = soup.find(id=f"postmenu_{post_id}")
            username = user_elem.get_text(strip=True) if user_elem else "Desconocido"

            # Mensaje
            msg_elem = soup.find(id=f"post_message_{post_id}")
            if msg_elem:
                message_raw = msg_elem.get_text(separator="\n", strip=True)
            else:
                message_raw = ""

            # Extrae citas y texto propio
            message_text, quotes = extract_quotes_and_text(message_raw)
            mentions = extract_mentions(message_text)

            # Número de mensaje
            msg_num = None
            msg_num_elem = post_div.find("div", class_="date-and-time-gray", style=lambda s: s and "text-decoration: underline" in s)
            if msg_num_elem:
                msg_num = msg_num_elem.get_text(strip=True).replace("#", "")

            post_obj = {
                "post_id": post_id,
                "msg_num": msg_num,
                "username": username,
                "message": message_text,
                "quotes": quotes,
                "mentions": mentions
            }
            # Añade el post a la lista temporal para buscar citas
            if posts_so_far is not None:
                find_quoted_post_id(quotes, posts_so_far + posts)
            posts.append(post_obj)

        return posts