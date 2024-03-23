"""
::::::   ::::::  ::::::::  :::::  :::::   :::::  ::::::  ::::::  
:::::::::::::::  :::::     :::::  :::::   :::::  ::::::::::::::  
::::::   ::::::  :::::     :::::  :::::   :::::  ::::::::::::::  
::::::   ::::::  ::::::::  ::::::::::::   :::::  ::::::  ::::::  

"""
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from urllib3.exceptions import LocationParseError

def check_websites(urls):
    pages_loaded = 0
    pages_failed = 0
    
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"La página {url} se cargó correctamente.")
                take_screenshot(url)
                pages_loaded += 1
            else:
                print(f"La página {url} no se pudo cargar (código de estado: {response.status_code}).")
                pages_failed += 1
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a la página {url}: {str(e)}")
            pages_failed += 1
        except LocationParseError:
            print(f"Error de URL inválida para la página {url}.")
            pages_failed += 1

    print(f"\nCantidad de páginas cargadas correctamente: {pages_loaded}")
    print(f"Cantidad de páginas que no se pudieron cargar: {pages_failed}")

def take_screenshot(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(2)  # Esperar 2 segundos para que la página se cargue completamente
        
        parsed_url = urlparse(url)
        filename = parsed_url.netloc + parsed_url.path
        filename = filename.replace("/", "_")  # Reemplazar "/" con "_" en la ruta para evitar problemas con el nombre del archivo
        driver.save_screenshot(f"screenshot_{filename}.png")
        driver.quit()
        
        print(f"Se tomó el screenshot de {url} correctamente.")
    except Exception as e:
        print(f"Error al tomar el screenshot de {url}: {str(e)}")
        driver.quit()


# Solicitar al usuario ingresar las URLs
print("Ingresa las URLs para tomar los screenshots (ingresa 'fin' para terminar):")
urls = []
while True:
    url = input("URL: ")
    if url.lower() == "fin":
        break
    urls.append(url)

# Verificar y tomar los screenshots de las URLs ingresadas
check_websites(urls)

# Imprimir los resultados finales y agregar una pausa para mantener la consola abierta
print("\nProceso completado.")
input("Presiona Enter para salir...")

