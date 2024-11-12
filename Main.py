import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Crear el libro de trabajo y la hoja
workbook = Workbook()
sheet = workbook.active
sheet.title = "IMDb Top 250 Movies"
sheet.append(['Number', 'Movie URL', 'Movie Name', 'Movie Year'])

# URL de IMDb para las mejores películas
url = "https://www.imdb.com/chart/top"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}

# Hacer la solicitud
response = requests.get(url, headers=headers)

# Verificar el código de estado
if response.status_code != 200:
    print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")
    exit()

# Parsear el contenido HTML de la página
soup = BeautifulSoup(response.content, 'lxml')

# Encontrar las películas en el ranking
movies = soup.find_all('td', class_='titleColumn')

num = 0

for movie in movies:
    num += 1
    try:
        # Obtener el nombre y el año de la película
        movie_name = movie.a.text
        movie_year = movie.span.text.strip('()')  # Eliminar los paréntesis

        # Obtener la URL de la película
        movie_url = 'https://www.imdb.com' + movie.a['href']

        # Escribir los datos en el archivo de Excel
        sheet.append([num, movie_url, movie_name, movie_year])

        print(f"{num}. {movie_name} - {movie_year} - {movie_url}")
    
    except Exception as e:
        print(f"Error processing movie: {e}")
        continue

# Guardar el archivo de Excel
workbook.save('imdb_top_250_movies.xlsx')
print("Data has been saved to imdb_top_250_movies.xlsx")
