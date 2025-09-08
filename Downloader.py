import time

import requests
from bs4 import BeautifulSoup
import os

def urjc_downloader():
    # URL de la page à scanner
    url = "https://www.urjc.es/i-d-i/servicio-contratacion/4608-convocatorias-con-cargo-a-proyectos"

    # Télécharger la page
    response = requests.get(url)
    html = response.text

    # Parser le HTML
    soup = BeautifulSoup(html, "html.parser")

    # Trouver tous les liens PDF
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link['href']
        if href.lower().endswith("ca.pdf"):
            # URL complète si lien relatif
            if not href.startswith("http"):
                href = requests.compat.urljoin(url, href)
            pdf_links.append(href)

    print(f"{len(pdf_links)} PDF trouvés :")
    for pdf in pdf_links:
        print(pdf)

    output_dir = "urjc"
    os.makedirs(output_dir, exist_ok=True)

    for pdf_url in pdf_links:
        filename = os.path.join(output_dir, pdf_url.split("/")[-1])
        if os.path.exists(filename):
            continue
        else:
            r = requests.get(pdf_url)
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Descargado : {filename}")
            time.sleep(1)

urjc_downloader()