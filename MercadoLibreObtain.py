import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mercadolibre(product):
    # Reemplaza los espacios por guiones
    product = product.replace(" ", "-")
    precio = 0
    # Añade el texto product a la URL de Mercado Libre
    url = f"https://listado.mercadolibre.com.mx/{product}"

    # Impresión de la URL
    print(f"Buscando en {url} \n")

    # Hacer la solicitud HTTP a la página
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    # Crear una lista para almacenar los datos
    productos_data = []

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido de la página
        soup = BeautifulSoup(response.content, "html.parser")

        # Buscar el contenedor de productos
        contenedor_productos = soup.find_all("li", class_="ui-search-layout__item shops__layout-item")
        # Verificar si el contenedor de productos fue encontrado
        if contenedor_productos:
            print(f"Se encontraron {len(contenedor_productos)} productos.\n")

            # Iterar a través de cada producto en el contenedor
            for producto in contenedor_productos:
                # Extraer el enlace del producto y el título desde el <a> dentro del <h2> con la clase 'poly-box poly-component__title'
                h2_tag = producto.find("h2", class_="poly-box poly-component__title")
                if h2_tag:
                    link = h2_tag.find("a")
                    if link:
                        enlace = link["href"]
                        titulo_texto = link.text.strip()

                # Extraer el precio actual desde el contenedor 'poly-component__price'
                precio_contenedor = producto.find("div", class_="poly-component__price")
                if precio_contenedor:
                    # Extraer el precio actual
                    precio_actual = precio_contenedor.find("span", class_="andes-money-amount andes-money-amount--cents-superscript")
                    if precio_actual:
                        # Extraemos las partes del precio actual (fracción y centavos)
                        precio_actual_fraccion = precio_actual.find("span", class_="andes-money-amount__fraction")
                        if  precio_actual_fraccion:
                            precio = f"${precio_actual_fraccion.text}"
                # Verificar si el título, el enlace y el precio existen antes de agregar a la lista
                if titulo_texto and enlace and precio:
                    producto_info = {
                        'Producto': titulo_texto,
                        'Link': enlace,
                        'Precio Actual': precio
                    }
                    productos_data.append(producto_info)
                    print(f"{titulo_texto} - {precio} - {enlace}")

        else:
            print("No se encontró la lista de productos en la página.")
    else:
        print("Error al realizar la solicitud.")

    # Crear un DataFrame con los datos
    df = pd.DataFrame(productos_data)

    # Guardar el DataFrame en un archivo Excel
    if not df.empty:
        df.to_excel("productos_mercadolibre.xlsx", index=False)
        print("Los datos se han guardado correctamente en 'productos_mercadolibre.xlsx'.")
    else:
        print("No se encontraron productos para guardar.")
