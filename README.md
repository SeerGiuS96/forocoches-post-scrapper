# FC Post Scraper

Este proyecto nace de la curiosidad por analizar y aprender de los comentarios y experiencias compartidas por los usuarios de ForoCoches. Quería recopilar consejos, errores y anécdotas de los foreros, y de paso, practicar programación y scraping web con Python.

Elegí **Python** porque, aunque nunca lo había usado antes, es uno de los lenguajes más populares y versátiles. Es ideal para tareas de scraping y análisis de datos, así que me pareció la herramienta perfecta para experimentar y aprender algo nuevo.

## ¿Qué hace este scraper?

- Extrae todos los mensajes de un hilo de ForoCoches.
- Guarda el nombre de usuario, el mensaje, y las citas o respuestas a otros usuarios.
- Permite analizar fácilmente el contenido de cualquier hilo público.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/forocoches-post-scrapper.git
   cd forocoches-post-scrapper
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Abre el archivo `main.py` y **cambia el valor de `THREAD_ID`** por el ID del hilo que quieras analizar:
   ```python
   THREAD_ID = "10343939"  # Cambia este valor por el ID del hilo que te interese
   ```

2. Ejecuta el scraper:
   ```bash
   python main.py
   ```

3. Los datos extraídos se guardarán en `forocoches_posts.json`.

---

**¿Por qué este proyecto?**  
Me apetecía aprender de la comunidad de ForoCoches y, al mismo tiempo, mejorar mis habilidades técnicas. Python me ha permitido hacerlo de forma sencilla y potente.

¡Espero que te resulte útil o interesante!
