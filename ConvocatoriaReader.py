import os
import glob
from datetime import datetime

import pdfplumber
import pandas as pd
# import streamlit as st
import re

def load_text(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()

def detectar_universidad(path):
    mapping = {
        "uc3m": "Universidad Carlos III de Madrid",
        "uam": "Universidad Autónoma de Madrid",
        "urjc": "Universidad Rey Juan Carlos",
        "usal": "Universidad de Salamanca",
        "upm": "Universidad Politécnica de Madrid",
        # ... ajouter les autres
    }

    folder_name = os.path.dirname(path)
    for key, uni in mapping.items():
        if re.search(rf"\b{key}\b", folder_name):
            return uni
    return "Universidad desconocida"

def extract_fecha_firma(text):
    match = re.search(r"(\d{2}[-/]\d{2}[-/]\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if match:
        fecha_str, hora_str = match.groups()
        dt = datetime.strptime(f"{fecha_str} {hora_str}", "%d-%m-%Y %H:%M:%S")
        return dt  # datetime objet
    return None

def normalize_dataframe(df):

    column_order = ['referencia_interna', "puesto", 'titulo_proyecto',
                    'fecha_inicio_contrato', 'fecha_inicio_proyecto',
     'fecha_fin_proyecto', 'entidad_financiadora', 'investigador_principal',
     'centro', 'num_plazas', 'nivel_formativo',
     'salario_bruto_mensual', 'duracion_inicial',
     'dedicacion', 'tipo_contrato']

    for col in column_order:
        if col not in df.columns:
            df[col] = None

    # Reorder
    df = df[column_order]
    return df

def parse_offers(text: str):
    plazas = []

    # Découper en blocs
    bloques = re.split(r"PERFIL DEL PUESTO", text)
    del bloques[0]
    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue

        plaza = {}

        # Référence interne
        ref = re.search(r"Referencia Interna:\s*(\S+)", bloque)
        if ref:
            plaza["referencia_interna"] = ref.group(1)

        # Titre du projet
        titulo = re.search(r"T[ií]tulo del proyecto:\s*(.+)", bloque)
        if titulo:
            plaza["titulo_proyecto"] = titulo.group(1).strip()

        # Fechas
        fecha_inicio = re.search(r"Fecha inicio proyecto:\s*([\d/]+)", bloque)
        fecha_fin = re.search(r"Fecha fin del proyecto:\s*([\d/]+)", bloque)
        if fecha_inicio:
            plaza["fecha_inicio_proyecto"] = fecha_inicio.group(1)
        if fecha_fin:
            plaza["fecha_fin_proyecto"] = fecha_fin.group(1)

        # Entidad financiadora
        entidad = re.search(r"Entidad financiadora:\s*(.+)", bloque)
        if entidad:
            plaza["entidad_financiadora"] = entidad.group(1).strip()

        # Investigador principal
        ip = re.search(r"Investigador principal:\s*(.+)", bloque)
        if ip:
            plaza["investigador_principal"] = ip.group(1).strip()

        # Centro
        centro = re.search(r"Centro:\s*(.+)", bloque)
        if centro:
            plaza["centro"] = centro.group(1).strip()

        # Nº de plazas
        num_plazas = re.search(r"N[ºo]\s*de plazas convocadas:\s*(\d+)", bloque, re.IGNORECASE)
        if num_plazas:
            plaza["num_plazas"] = int(num_plazas.group(1))

        # Puesto
        puesto = re.search(r"Denominaci[oó]n del puesto:\s*(.+)", bloque)
        if puesto:
            plaza["puesto"] = puesto.group(1).strip()

        # Nivel formativo
        nivel = re.search(r"Nivel formativo:\s*(.+)", bloque)
        if nivel:
            plaza["nivel_formativo"] = nivel.group(1).strip()

        # Tipo de contrato
        contrato = re.search(r"Tipo de contrato:\s*(.+)", bloque)
        if contrato:
            plaza["tipo_contrato"] = contrato.group(1).strip()

        # Salario
        salario = re.search(r"Salario bruto mensual.*?:\s*([\d.,]+)", bloque)
        if salario:
            plaza["salario_bruto_mensual"] = salario.group(1)
        # Duración
        duracion = re.search(r"Duraci[oó]n inicial prevista:\s*(.+)", bloque)
        if duracion:
            plaza["duracion_inicial"] = duracion.group(1).strip()

        # Fecha inicio contrato
        fecha_contrato = re.search(r"Fecha estimada de inicio del contrato:\s*([\d/]+)", bloque)
        if fecha_contrato:
            plaza["fecha_inicio_contrato"] = fecha_contrato.group(1)

        # Dedicación
        dedicacion = re.search(r"Dedicaci[oó]n:\s*•?\s*(.+)", bloque)
        if dedicacion:
            plaza["dedicacion"] = dedicacion.group(1).strip()

        plazas.append(plaza)

    return plazas

class ConvocatoriaReader:
    def __init__(self, pdf_path):
        self.offers = None
        self.pdf_path = pdf_path
        txt_path = os.path.splitext(pdf_path)[0] + '.txt'
        if os.path.exists(txt_path):
            self.text = load_text(txt_path)
        else:
            with pdfplumber.open(self.pdf_path) as pdf:
                self.text = ""
                for page in pdf.pages:
                    self.text += page.extract_text() + "\n"
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(self.text)
        self.date = extract_fecha_firma(self.text)

    def get_offers(self):
        self.offers = pd.DataFrame(parse_offers(self.text))
        self.offers = normalize_dataframe(self.offers)

    def export_csv(self):
        self.offers.to_csv("offers.csv", index=False)

if __name__ == '__main__':
    pdf_path = "urjc/CP2303-5160_2_ca.pdf"
    #pdf_path = "uam/uam_convocatoria.pdf"
    reader = ConvocatoriaReader(pdf_path)
    # reader.get_offers()
    # reader.export_csv()