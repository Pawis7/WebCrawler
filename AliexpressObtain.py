import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_aliexpress(product):
    # Reemplaza los espacios por guiones
    product = product.replace(" ", "-")
    
    # URL base con el producto
    base_url = f"https://es.aliexpress.com/w/wholesale-{product}.html?spm"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    productos_data = []
    page = 1  # Empezamos con la primera página

    while True:  # Continuar hasta que no haya más productos
        url = f"{base_url}&page={page}"  # Modificar la URL para cambiar de página
        print(f"Buscando en {url} \n")

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            contenedor_productos = soup.find_all("div", class_="list--gallery--C2f2tvm search-item-card-wrapper-gallery")
            
            if contenedor_productos:
                print(f"Se encontraron {len(contenedor_productos)} productos en la página {page}.\n")
                
                for producto in contenedor_productos:
                    titulo = producto.find(class_="multi--title--G7dOCj3")
                    link = producto.find("a", class_="multi--container--1UZxxHY cards--card--3PJxwBm search-card-item")
                    precio_elemento = producto.find("div", class_="multi--price-sale--U-S0jtj")
                    precio_original = producto.find("div", class_="multi--price-original--1zEQqOK")
                    
                    if precio_elemento:
                        precio = "".join([span.text.strip() for span in precio_elemento.find_all("span") if span.text.strip()])
                        
                    if titulo and link and precio:
                        producto_info = {
                            'Producto': titulo['title'],
                            'Link': f"https:{link.get('href')}",
                            'Precio': precio
                        }
                        productos_data.append(producto_info)
                
                page += 1  # Incrementar el número de página
            else:
                print("No se encontró la lista de productos en la página.")
                break
        else:
            print("Error al realizar la solicitud.")
            break
    
    # Guardar los resultados en un archivo Excel
    df = pd.DataFrame(productos_data)

    if not df.empty:
        df.to_excel("productos_aliexpress.xlsx", index=False)
        print("Los datos se han guardado correctamente en 'productos_aliexpress.xlsx'.")
    else:
        print("No se encontraron productos para guardar.")
