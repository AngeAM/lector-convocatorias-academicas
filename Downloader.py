import time

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import pandas as pd
from datetime import datetime

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
    for link in soup.find_all("a", string="Convocatoria y Anexo Plazas"):
        href = link['href']
        pdf_links.append(href)
    pdf_links.reverse()
    pdf_links = pdf_links[:3]

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

def ucm_downloader():
    pdf_links = []
    base_url = "https://www.ucm.es"

    # get the last convocatoria in PLI===========================================
    main_url = "https://www.ucm.es/personal-contratado-de-actividades-cientifico-tecnicas-pli-ucm"
    resp = requests.get(main_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Chercher le lien qui contient "Última convocatoria"
    ultima = soup.find("h2", string="Última convocatoria")
    if ultima:
        div = ultima.find_parent()
        link = div.find_all("a")[-1]["href"]
        link = urljoin(base_url, link)
    else:
        print("No he encontrado una ultima convocatoria")
    resp2 = requests.get(link)
    soup2 = BeautifulSoup(resp2.text, "html.parser")
    url_anexo_pli = soup2.find("a", string="Anexo de plazas convocadas")["href"]
    pdf_links.append(url_anexo_pli)

    # get the convocatorias from PAI=============================================
    main_url = "https://www.ucm.es/personal-de-apoyo-a-la-investigacion-pai-ucm"
    resp = requests.get(main_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # Chercher le lien qui contient "Última convocatoria"
    ultima = soup.find_all("h2", string="Última convocatoria")
    if ultima:
        div_paii = ultima[0].find_parent()
        div_pait = ultima[1].find_parent()
        if "abierta" in div_paii.find("img")["src"]:
            link_paii = div_paii.find_all("a")[-1]["href"]
            link_paii = urljoin(base_url, link_paii)
            resp_paii = requests.get(link_paii)
            soup_paii = BeautifulSoup(resp_paii.text, "html.parser")
            url_anexo_paii = soup_paii.find("a", string="Anexo de plazas convocadas")["href"]
            pdf_links.append(url_anexo_paii)

        if "abierta" in div_pait.find("img")["src"]:
            link_pait = div_pait.find_all("a")[-1]["href"]
            link_pait = urljoin(base_url, link_pait)
            resp_pait = requests.get(link_pait)
            soup_pait = BeautifulSoup(resp_pait.text, "html.parser")
            url_anexo_pait = soup_pait.find("a", string="Anexo de plazas convocadas")["href"]
            pdf_links.append(url_anexo_pait)
    else:
        print("No he encontrado ultimas convocatorias")
    output_dir = "ucm"
    for pdf_url in pdf_links:
        filename = os.path.join(output_dir, pdf_url.split("/")[-1].split("?")[0]+".pdf")
        if os.path.exists(filename):
            continue
        else:
            r = requests.get(pdf_url)
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"Descargado : {filename}")
            time.sleep(1)

def uam_downloader():
    # URL de la page à scanner
    url = "https://www.uam.es/uam/investigacion/ofertas-empleo"

    # Télécharger la page
    response = requests.get(url)
    html = response.text

    # Parser le HTML
    soup = BeautifulSoup(html, "html.parser")
    soup_ofertas = soup.find_all("a", attrs={"class": "uam-becas-card"})[:10]
    ofertas_uam = {}
    title = []
    date = []
    for sub_soup in soup_ofertas:
        if "abierta" in sub_soup["data-tag"]:
            title.append(sub_soup.find_all("p")[-1].text)
            date.append(sub_soup.find_all("span")[-1].text)
    ofertas_uam["title"] = title
    ofertas_uam["date"] = date
    ofertas_uam = pd.DataFrame(ofertas_uam)
    ofertas_uam.to_csv("uam/ofertas_uam.csv", index=False)

def uc3m_downloader():
    # URL de la page à scanner
    url = "https://aplicaciones.uc3m.es/atenea/publico/1/listarConvocatorias"
    # Télécharger la page
    response = requests.get(url)
    html = response.text
    ofertas_uc3m = {}
    date = []
    fecha_sol_inicio = []
    title = []
    IP = []
    estado = []
    fecha_sol_fin = []
    codigo = []
    # Parser le HTML
    soup = BeautifulSoup(html, "html.parser")
    soup_ofertas = soup.find_all("tr")

    for sub_soup in soup_ofertas:
        soup_offer = sub_soup.find_all("td")
        if len(soup_offer) < 6:
            continue
        if "RESUELTA" not in soup_offer[5].text:
            codigo.append(soup_offer[0].text)
            title.append(soup_offer[1].text)
            IP.append(soup_offer[2].text)
            estado.append(soup_offer[5].text)
            fecha_sol_inicio.append(soup_offer[3].text)
            # conversion date
            try:
                date.append(datetime.strptime(soup_offer[3].text, "%d/%m/%Y"))
            except ValueError:
                date.append(None)
            fecha_sol_fin.append(soup_offer[4].text)

    ofertas_uc3m["date"] = date
    ofertas_uc3m["IP"] = IP
    ofertas_uc3m["estado"] = estado
    ofertas_uc3m["fecha_sol_fin"] = fecha_sol_fin
    ofertas_uc3m["fecha_sol_inicio"] = fecha_sol_inicio
    ofertas_uc3m["codigo"] = codigo
    ofertas_uc3m["title"] = title
    column_order = ["codigo", "title","fecha_sol_inicio","fecha_sol_fin", "IP", "estado", "date"]
    ofertas_uc3m = pd.DataFrame(ofertas_uc3m, columns=column_order)
    ofertas_uc3m = ofertas_uc3m.sort_values(by="date", ascending=False).reset_index(drop=True)
    del ofertas_uc3m["date"]
    ofertas_uc3m.to_csv("uc3m/ofertas_uc3m.csv", index=False)

def upm_downloader():
    # URL de la page à scanner
    url = "https://web.upm.es/hrs4r/"
    # Télécharger la page
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    soup_ofertas = soup.find_all("div", attrs={"class": "card-body"})

    ofertas_upm = {
        "codigo": [],
        "title": [],
        "centro": [],
        "date": [],
        "IP": [],
        "fecha_sol_inicio": [],
        "fecha_sol_fin": [],
    }

    for sub_soup in soup_ofertas:
        soup_offer = sub_soup.find_all("div")
        ofertas_upm["title"].append(sub_soup.find("h4").text.strip())
        ofertas_upm["codigo"].append(soup_offer[0].text.strip())
        ofertas_upm["centro"].append(soup_offer[1].text.strip())
        ofertas_upm["IP"].append(soup_offer[3].find("p").text)
        ofertas_upm["fecha_sol_inicio"].append(soup_offer[4].find("time").text)
        ofertas_upm["fecha_sol_fin"].append(soup_offer[5].find("time").text)
        date = soup_offer[4].find("time")["datetime"]
        date = datetime.fromisoformat(date.replace("Z", "+00:00"))
        ofertas_upm["date"].append(date)

    column_order = ["codigo", "title", "centro" "fecha_sol_inicio", "fecha_sol_fin", "IP", "date"]
    ofertas_upm = pd.DataFrame(ofertas_upm)
    ofertas_upm = ofertas_upm.sort_values(by="date", ascending=False).reset_index(drop=True)
    del ofertas_upm["date"]
    ofertas_upm.to_csv("upm/ofertas_upm.csv", index=False)









