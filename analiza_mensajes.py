import json
from collections import defaultdict

# Carga el JSON
with open("forocoches_posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

CATEGORIES = {
    "negocios": [
        "negocio", "empresa", "emprender", "autónomo", "sociedad", "startup", "facturación", "factura", "proveedor", "cliente"
    ],
    "bolsa": [
        "bolsa", "acciones", "dividendos", "ibex", "nasdaq", "mercado bursátil", "broker", "wall street", "etf", "fondos de inversión", "renta variable", "renta fija", "sp500"
    ],
    "criptomonedas": [
        "cripto", "bitcoin", "ethereum", "btc", "eth", "blockchain", "altcoin", "wallet", "moneda digital", "exchange", "binance", "coinbase", "dogecoin", "nft"
    ],
    "pisos": [
        "piso", "vivienda", "alquiler", "hipoteca", "casa", "inmobiliaria", "arrendar", "inquilino", "propietario",
        "reforma", "obra nueva", "promotor", "apartamento", "ático", "chalet", "terreno", "solar", "urbanización",
        "comunidad de vecinos", "vecinos", "inmueble", "inmuebles", "promoción inmobiliaria", "okupa", "ocupa"
    ],
    "coches": [
        "coche", "vehículo", "auto", "concesionario", "km", "motor", "gasolina", "diésel", "eléctrico", "híbrido", "itv", "seguro de coche", "matrícula", "garaje", "taller", "mecánico", "reparación", "carnet de conducir", "permiso de conducir", "renting", "leasing"
    ],
    "trabajo": [
        "trabajo", "empleo", "currar", "oficina", "jefe", "despido", "contrato laboral", "sueldo", "salario", "nómina", "paro", "oposición", "funcionario", "teletrabajo", "entrevista de trabajo", "currículum", "prácticas", "beca"
    ],
    "relaciones": [
        "novia", "pareja", "relación", "matrimonio", "casarse", "divorcio", "ex", "amor", "ligar", "cita", "infidelidad", "ruptura", "amistad", "tinder", "badoo", "hijos", "familia", "padres", "madre", "padre"
    ],
    "otros": []
}

def categorize_message(msg):
    msg_l = msg.lower()
    cats = []
    for cat, keywords in CATEGORIES.items():
        if cat == "otros":
            continue
        if any(kw in msg_l for kw in keywords):
            cats.append(cat)
    if not cats:
        cats = ["otros"]
    return cats

def format_message(post, posts_by_user):
    html_msg = ""
    for quote in post.get("quotes", []):
        quoted_user = quote.get("quoted_user", "")
        quoted_post_id = quote.get("quoted_post_id")
        if quoted_post_id:
            quoted_link = f' <a href="#post_{quoted_post_id}">(ver mensaje)</a>'
            html_msg += (
                f'<div style="border-left: 4px solid #aaa; background: #f0f0f0; margin: 0.5em 0; padding: 0.5em 1em;">'
                f'<b>{quoted_user}</b>{quoted_link}</div>'
            )
        else:
            quoted_text = quote.get("quoted_text", "")
            html_msg += (
                f'<div style="border-left: 4px solid #aaa; background: #f0f0f0; margin: 0.5em 0; padding: 0.5em 1em;">'
                f'<b>{quoted_user}:</b><br>{quoted_text.replace(chr(10), "<br>")}</div>'
            )
    # Texto propio
    if post["message"].strip():
        # Menciones
        msg = post["message"]
        for mention in post.get("mentions", []):
            msg = msg.replace(f"@{mention}", f'<span style="color:#0074d9">@{mention}</span>')
        html_msg += f'<div>{msg.replace(chr(10), "<br>")}</div>'
    return html_msg

# Agrupa mensajes por usuario para enlazar citas
posts_by_user = defaultdict(list)
for post in posts:
    posts_by_user[post["username"]].append(post)

# Agrupa mensajes por categoría (permitiendo que estén en varias)
categorias = defaultdict(list)
for post in posts:
    cats = categorize_message(post["message"])
    for cat in cats:
        if post not in categorias[cat]:
            categorias[cat].append(post)

# Ordena categorías por número de mensajes (de mayor a menor)
categorias_ordenadas = sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True)

# Genera HTML interactivo
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resumen ForoCoches por Categorías</title>
    <style>
    body { font-family: Arial, sans-serif; background: #f9f9f9; color: #222; }
    h1 { text-align: center; }
    details { margin-bottom: 1em; background: #fff; border-radius: 6px; box-shadow: 0 2px 8px #0001; }
    summary { font-size: 1.2em; font-weight: bold; cursor: pointer; padding: 10px; }
    .msg { margin: 0.5em 1.5em; padding: 0.5em; border-bottom: 1px solid #eee; background: #f5f5f5; border-radius: 4px; }
    .count { color: #888; font-size: 0.95em; }
    </style>
</head>
<body>
<h1>Resumen ForoCoches por Categorías</h1>
"""

for cat, posts_cat in categorias_ordenadas:
    html += f'<details><summary>{cat.capitalize()} <span class="count">({len(posts_cat)} mensajes)</span></summary>\n'
    for post in posts_cat:
        username = post.get("username", "")
        msg_html = format_message(post, posts_by_user)
        html += f'<div class="msg" id="post_{post["post_id"]}"><b>{username}:</b> {msg_html}</div>\n'
    html += '</details>\n'

html += """
</body>
</html>
"""

with open("forocoches_post_resumen.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Resumen interactivo generado en forocoches_post_resumen.html")