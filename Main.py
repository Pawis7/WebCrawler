import requests
from bs4 import BeautifulSoup
import pandas as pd

# Paso 1: Definir la URL de la página principal de Wikipedia
url = 'https://es.wikipedia.org/wiki/Wikipedia:Portada'

# Paso 2: Realizar la solicitud HTTP para obtener el contenido de la página
print(f"Realizando solicitud a la URL: {url}")
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    print("Página descargada con éxito.")
    
    # Paso 3: Parsear el contenido HTML usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Paso 4: Buscar los artículos destacados o cualquier sección que te interese
    articles = []

    # Buscamos enlaces en todas las secciones relevantes (por ejemplo, "Artículos destacados")
    print("Extrayendo artículos...")
    for link in soup.find_all('a', href=True):
        title = link.get_text(strip=True)  # Obtiene el texto del enlace
        url = link['href']
        
        # Filtramos solo enlaces relevantes, los que están en la sección de artículos destacados
        if title and url.startswith('/wiki/'):
            # Creamos la URL completa
            full_url = 'https://es.wikipedia.org' + url
            articles.append((title, full_url))

    # Verificar cuántos artículos se extrajeron
    print(f"Se extrajeron {len(articles)} artículos.")

    # Paso 5: Crear un DataFrame de pandas con los títulos y enlaces de los artículos
    df = pd.DataFrame(articles, columns=['Título', 'URL'])

    # Mostrar las primeras filas para verificar que los datos son correctos
    print("\nPrimeros artículos extraídos:")
    print(df.head())  # Muestra las primeras 5 filas

    # Paso 6: Guardar la información en un archivo Excel
    print("\nGuardando los datos en un archivo Excel...")
    df.to_excel('articulos_destacados_wikipedia.xlsx', index=False, engine='openpyxl')

    print("Los datos fueron guardados en 'articulos_destacados_wikipedia.xlsx'.")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
