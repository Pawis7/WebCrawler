from AliexpressObtain import scrape_aliexpress
from MercadoLibreObtain import scrape_mercadolibre

# Solicita el producto al usuario
product = input("Introduce el producto que deseas buscar: ")

# Llama a la función de scraping pasando el producto
scrape_aliexpress(product)
scrape_mercadolibre(product)
