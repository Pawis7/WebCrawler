import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Lista de posibles User-Agents para rotar entre ellos
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.49"
]

def scrape_mercadolibre(product):
    # Reemplaza los espacios por guiones
    product = product.replace(" ", "-")
    precio = 0
    # URL de búsqueda en Mercado Libre
    url = f"https://listado.mercadolibre.com.mx/{product}"

    print(f"Buscando en {url} \n")

    # Selección aleatoria de un User-Agent
    headers = {
        "User-Agent": random.choice(user_agents)
    }

    # Realizar la solicitud HTTP
    response = requests.get(url, headers=headers)

    # Crear lista para almacenar los datos
    productos_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        contenedor_productos = soup.find_all("li", class_="ui-search-layout__item shops__layout-item") or soup.find_all("li", class_="ui-search-layout__item")
        
        if contenedor_productos:
            print(f"Se encontraron {len(contenedor_productos)} productos.\n")

            for producto in contenedor_productos:
                h2_tag = producto.find("h2", class_="poly-box poly-component__title")
                if h2_tag:
                    link = h2_tag.find("a")
                    if link:
                        enlace = link["href"]
                        titulo_texto = link.text.strip()

                precio_contenedor = producto.find("div", class_="poly-component__price")
                if precio_contenedor:
                    precio_actual = precio_contenedor.find("span", class_="andes-money-amount andes-money-amount--cents-superscript")
                    if precio_actual:
                        precio_actual_fraccion = precio_actual.find("span", class_="andes-money-amount__fraction")
                        if precio_actual_fraccion:
                            precio = f"${precio_actual_fraccion.text}"
                
                # Verificar si el título, el enlace y el precio existen antes de agregar a la lista
                if titulo_texto and enlace and precio:
                    producto_info = {
                        'Etiqueta': 'Mercado Libre',
                        'Producto': titulo_texto,
                        'Link': enlace,
                        'Precio': precio
                    }
                    productos_data.append(producto_info)
                    print(f"{titulo_texto} - {precio} - {enlace}")

        else:
            print("No se encontró la lista de productos en la página.")
    else:
        print("Error al realizar la solicitud.")

    # Crear un DataFrame con los datos
    df = pd.DataFrame(productos_data)

    # Guardar los resultados en un archivo Excel
    if not df.empty:
        df.to_excel("mercadolibre.xlsx", index=False)
        print("Los datos se han guardado correctamente en 'productos_mercadolibre.xlsx'.")
    else:
        print("No se encontraron productos para guardar.")

    # Esperar un tiempo aleatorio entre solicitudes para evitar bloqueos
    time.sleep(random.randint(2, 5))  # Retraso de 2 a 5 segundos

