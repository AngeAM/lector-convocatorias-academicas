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
        "ucm": "Universidad Complutense de Madrid",
        # ... ajouter les autres
    }

    folder_name = os.path.dirname(path)
    for key, uni in mapping.items():
        if re.search(rf"\b{key}\b", folder_name):
            return uni
    return "Universidad desconocida"

def extract_fecha_firma_urjc(text):
    match = re.search(r"(\d{2}[-/]\d{2}[-/]\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if match:
        fecha_str, hora_str = match.groups()
        dt = datetime.strptime(f"{fecha_str} {hora_str}", "%d-%m-%Y %H:%M:%S")
        return dt  # datetime objet
    return None

def parse_offers_urjc(text: str):
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
        fecha_contrato = re.search(r"Fecha estimada de inicio del contrato:\s*(.+)", bloque)
        if fecha_contrato:
            plaza["fecha_inicio_contrato"] = fecha_contrato.group(1)

        # Dedicación
        dedicacion = re.search(r"Dedicaci[oó]n:\s*•?\s*(.+)", bloque)
        if dedicacion:
            plaza["dedicacion"] = dedicacion.group(1).strip()

        plazas.append(plaza)
    date = extract_fecha_firma_urjc(text)
    offers = pd.DataFrame(plazas)
    offers["fecha de publicacion"] = date.strftime("%d-%m-%Y")  # sera répétée pour toutes les lignes
    df = offers
    column_order = ["fecha de publicacion", "puesto", 'titulo_proyecto',
                    'fecha_inicio_contrato', 'investigador_principal',
                    'centro', 'num_plazas', 'nivel_formativo',
                    'salario_bruto_mensual', 'entidad_financiadora', 'duracion_inicial',
                    'fecha_inicio_proyecto',
                    'fecha_fin_proyecto',
                    'dedicacion', 'tipo_contrato', "referencia_interna"]
    # Reorder
    df = df[column_order]

    return df, date

def parse_offers_ucm(text: str):
    plazas = []

    # Découper par "CÓDIGO DE LA PLAZA"
    bloques = re.split(r"CÓDIGO DE LA PLAZA:", text)
    del bloques[0]

    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue

        plaza = {}

        # Código de la plaza
        codigo = re.match(r"(\S+)", bloque)
        if codigo:
            plaza["codigo_plaza"] = codigo.group(1)

        # Referencia plaza
        ref_plaza = re.search(r"REFERENCIA PLAZA:\s*(\S+)", bloque)
        if ref_plaza:
            plaza["referencia_interna"] = ref_plaza.group(1)

        # Línea de investigación
        linea = re.search(r"L[IÍ]NEA DE INVESTIGACI[ÓO]N:\s*(.+)", bloque)
        if linea:
            plaza["linea_investigacion"] = linea.group(1).strip()

        # Proyecto de investigación
        proyecto = re.search(r"PROYECTO DE INVESTIGACI[ÓO]N:\s*(.+)", bloque)
        if proyecto:
            plaza["titulo_proyecto"] = proyecto.group(1).strip()

        # # Referencia proyecto
        # ref_proy = re.search(r"REFERENCIA PROYECTO:\s*(\S+)", bloque)
        # if ref_proy:
        #     plaza["referencia_proyecto"] = ref_proy.group(1)

        # Número de plazas
        num_plazas = re.search(r"N[ÚU]MERO DE PLAZAS:\s*(\d+)", bloque)
        if num_plazas:
            plaza["num_plazas"] = int(num_plazas.group(1))

        # Investigador principal
        ip = re.search(r"INVESTIGADOR PRINCIPAL:\s*(.+)", bloque)
        if ip:
            plaza["investigador_principal"] = ip.group(1).strip()

        # # Departamento
        # dept = re.search(r"DEPARTAMENTO INCORPORACI[ÓO]N:\s*(.+)", bloque)
        # if dept:
        #     plaza["departamento"] = dept.group(1).strip()

        # Centro
        centro = re.search(r"CENTRO:\s*(.+)", bloque)
        if centro:
            plaza["centro"] = centro.group(1).strip()

        # Categoría
        categoria = re.search(r"CATEGOR[IÍ]A:\s*(.+)", bloque)
        if categoria:
            plaza["categoria"] = categoria.group(1).strip()

        # Titulación requerida
        titulacion = re.search(r"TITULACI[ÓO]N REQUERIDA:\s*(.+)", bloque)
        if titulacion:
            plaza["nivel_formativo"] = titulacion.group(1).strip()

       # Tareas
        tareas = re.search(r"TAREAS A REALIZAR:\s*(.+?)M[ÉE]RITOS", bloque, re.S)
        if tareas:
            plaza["tareas"] = tareas.group(1).strip()

        # Fechas
        fecha_inicio = re.search(r"FECHA INICIO CONTRATO.*?:\s*([\d/.-]+)", bloque)
        if fecha_inicio:
            plaza["fecha_inicio_contrato"] = fecha_inicio.group(1)

        fecha_fin = re.search(r"FECHA DE FINALIZACI[ÓO]N.*?:\s*(.+)", bloque)
        if fecha_fin:
            plaza["fecha_fin_contrato"] = fecha_fin.group(1).strip()

        # Dedicación
        dedicacion = re.search(r"DEDICACI[ÓO]N:\s*(.+)", bloque)
        if dedicacion:
            plaza["dedicacion"] = dedicacion.group(1).strip()

        # Salario
        salario = re.search(r"SALARIO MES:\s*(.+)", bloque)
        if salario:
            plaza["salario"] = salario.group(1).strip()

        plazas.append(plaza)

    df = pd.DataFrame(plazas)
    column_order = ['titulo_proyecto',  'linea_investigacion', 'centro',
                    'fecha_inicio_contrato','fecha_fin_contrato',
        'tareas','num_plazas', 'investigador_principal',
       'categoria', 'nivel_formativo', 'salario',
        'dedicacion',  'referencia_interna', 'codigo_plaza', ]
    # Reorder
    df = df[column_order]

    return df

    return plazas

def pase_offers_uam(text: str):
    return None


class ConvocatoriaReader:
    def __init__(self, pdf_path):
        self.date = None
        self.offers = None
        self.pdf_path = pdf_path
        self.uni = detectar_universidad(self.pdf_path)
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


    def get_offers(self):
        if self.uni == "Universidad Rey Juan Carlos":
            self.offers, self.date = parse_offers_urjc(self.text)
        elif self.uni == "Universidad Complutense de Madrid":
            self.offers = parse_offers_ucm(self.text)
        elif self.uni == "Universidad Autónoma de Madrid":
            self.offers, self.date = parse_offers_ucm(self.text)
        return self.offers, self.date

    def export_csv(self):
        self.offers.to_csv("offers.csv", index=False)

if __name__ == '__main__':
    pdf_path = "urjc/Vice_Inv_Inn_05-25_ca.pdf"
    pdf_path = "ucm/02-anexo-convocatoria-paii57-13-25.pdf"
    reader = ConvocatoriaReader(pdf_path)
    reader.get_offers()
    # reader.export_csv()