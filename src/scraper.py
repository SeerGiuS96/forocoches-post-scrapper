from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class ForoCochesScraper:
    def scrape_thread(self, html):
        logger.info("Extrayendo posts...")
        soup = BeautifulSoup(html, "html.parser")
        posts_div = soup.find("div", id="posts")
        if not posts_div:
            logger.warning("No se encontró el contenedor de posts")
            return []

        posts = []
        # Busca todos los divs cuyo id empieza por 'edit'
        for post_div in posts_div.find_all("div", id=lambda x: x and x.startswith("edit")):
            post_id = post_div.get("id")[4:]  # Quita 'edit' del id para obtener el id numérico

            # Nombre de usuario
            user_elem = soup.find(id=f"postmenu_{post_id}")
            username = user_elem.get_text(strip=True) if user_elem else "Desconocido"

            # Mensaje
            msg_elem = soup.find(id=f"post_message_{post_id}")
            if msg_elem:
                # El mensaje puede estar en un <div> con tablas dentro
                message = msg_elem.get_text(separator="\n", strip=True)
            else:
                message = ""

            # Número de mensaje (busca el div con class 'date-and-time-gray' y subrayado)
            msg_num = None
            msg_num_elem = post_div.find("div", class_="date-and-time-gray", style=lambda s: s and "text-decoration: underline" in s)
            if msg_num_elem:
                msg_num = msg_num_elem.get_text(strip=True).replace("#", "")

            posts.append({
                "post_id": post_id,
                "username": username,
                "message": message,
                "msg_num": msg_num
            })

        return posts