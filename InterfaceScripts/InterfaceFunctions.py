from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from Scrapers.AliexpressObtain import scrape_aliexpress
from Scrapers.MercadoLibreObtain import scrape_mercadolibre
from InterfaceScripts.MainInterface import Ui_MainWindow
from PySide6.QtGui import QIcon
import pandas as pd  # Para manejar los archivos Excel
import sys
import os
import webbrowser
from PySide6.QtWidgets import QTableWidget  # Asegurando que importamos QTableWidget correctamente

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('Assets/icon.png'))  # Asegúrate de proporcionar la ruta correcta
        self.setWindowTitle("Pawis Web Scraper/Crawler")

        # Conectar el botón "Buscar" con la función
        self.ui.pushButton.clicked.connect(self.search_product)

        # Deshabilitar la ordenación automática en toda la tabla
        self.ui.tableWidget.setSortingEnabled(False)

        # Asegúrate de que el link en la tabla sea clickeable
        self.ui.tableWidget.cellClicked.connect(self.open_link)

        # Hacer que las celdas no sean editables
        self.ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.ui.label_3.mousePressEvent = self.open_link_on_click
        self.ui.label_4.mousePressEvent = self.open_link_on_click
        
    def search_product(self):
        # Obtener el texto del campo de entrada
        product = self.ui.lineEdit.text()

        # Validar si el campo está vacío
        if not product.strip():
            QMessageBox.warning(self, "Error", "Debe ingresar un producto")
            return

        try:
            # Ejecutar las funciones de scraping
            scrape_aliexpress(product)  # Se espera que genere un archivo Excel
            scrape_mercadolibre(product)  # Se espera que genere un archivo Excel

            # Verificar que los archivos existan
            if not os.path.exists("aliexpress.xlsx") or not os.path.exists("mercadolibre.xlsx"):
                QMessageBox.warning(self, "Error", "Los archivos de productos no se generaron correctamente.")
                return

            # Leer y combinar los datos de los archivos generados
            aliexpress_data = pd.read_excel("aliexpress.xlsx")  # Asegúrate del nombre correcto
            mercadolibre_data = pd.read_excel("mercadolibre.xlsx")  # Asegúrate del nombre correcto

            combined_data = pd.concat([aliexpress_data, mercadolibre_data], ignore_index=True)

            # Limpiar la columna de precios eliminando $ y comas
            combined_data["Precio"] = combined_data["Precio"].replace({r"\$": "", r",": ""}, regex=True)

            # Convertir la columna de precios a tipo float
            combined_data["Precio"] = pd.to_numeric(combined_data["Precio"], errors='coerce')

            # Filtrar los precios para asegurarnos de que solo haya valores válidos
            combined_data = combined_data[combined_data["Precio"].notna()]

            # Guardar los datos en un atributo para usarlos más tarde
            self.data = combined_data

            # Mostrar los datos en la tabla
            self.display_table(combined_data)
            
            #eliminar los archivos generados
            os.remove("aliexpress.xlsx")
            os.remove("mercadolibre.xlsx")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")

    def display_table(self, data):
        """
        Muestra los datos filtrados en la tabla de la interfaz.
        """
        self.ui.tableWidget.clear()  # Limpiar la tabla
        self.ui.tableWidget.setRowCount(len(data))  # Establecer el número de filas
        self.ui.tableWidget.setColumnCount(len(data.columns))  # Establecer el número de columnas
        self.ui.tableWidget.setHorizontalHeaderLabels(data.columns)  # Usar las etiquetas del archivo Excel
        
        # Añadir $ a la columna de precios
        data["Precio"] = data["Precio"].apply(lambda x: f"${x:.2f}")
        
        # Llenar la tabla con los datos
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                # Crear el elemento de la celda
                item = QTableWidgetItem(str(value))

                # Añadir el elemento a la tabla
                self.ui.tableWidget.setItem(row_idx, col_idx, item)

        # Hacer que las columnas ajusten su tamaño automáticamente
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def open_link(self, row, col):
        """
        Abre el enlace al hacer clic en la celda del enlace.
        """
        # Verificar si la columna seleccionada es la de "Link"
        if col == 2:  # Índice de la columna de "Link"
            link = self.ui.tableWidget.item(row, col).text()
            webbrowser.open(link)
    
    def open_link_on_click(self, event):
        """
        Abre el enlace al hacer clic en la imagen.
        """
        webbrowser.open("https://www.pawstudio.xyz")
