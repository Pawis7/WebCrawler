import requests
from bs4 import BeautifulSoup
import pandas as pd

# Paso 1: Definir la URL de la página principal de Wikipedia
url = 'https://es.wikipedia.org/wiki/Wikipedia:Portada'

# Paso 2: Realizar la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    # Paso 3: Parsear el contenido HTML usando BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Paso 4: Buscar los artículos destacados o cualquier sección que te interese
    # Para este caso, vamos a buscar los artículos destacados
    articles = []

    # Buscamos todos los enlaces dentro de la sección "Artículos destacados"
    for item in soup.find_all('div', class_='mp-upper'):
        for link in item.find_all('a', href=True):
            title = link.get_text()
            url = 'https://es.wikipedia.org' + link['href']  # Crear URL completa
            articles.append((title, url))

    # Paso 5: Crear un DataFrame de pandas con los títulos y enlaces de los artículos
    df = pd.DataFrame(articles, columns=['Título', 'URL'])

    # Paso 6: Guardar la información en un archivo Excel
    df.to_excel('articulos_destacados_wikipedia.xlsx', index=False, engine='openpyxl')

    print("Los datos fueron guardados en 'articulos_destacados_wikipedia.xlsx'.")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
