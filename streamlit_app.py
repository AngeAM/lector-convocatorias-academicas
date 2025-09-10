import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from OfferMerger import OfferMerger
from Downloader import *


urjc_downloader()
ucm_downloader()
uam_downloader()
uc3m_downloader()
upm_downloader()

OfferM = OfferMerger(["urjc", "ucm"])

st.set_page_config(layout="wide")

#=============URJC=========================================================================
st.markdown("# Ofertas de la Universidad Rey Juan Carlos (URJC)")
st.markdown("Convocatorias con cargo a proyectos: "
            "[https://www.urjc.es/i-d-i/servicio-contratacion/4608-convocatorias-con-cargo-a-proyectos]"
            "(https://www.urjc.es/i-d-i/servicio-contratacion/4608-convocatorias-con-cargo-a-proyectos)")
df = OfferM.merged_offers["urjc"]
col_defs = []
for c in df.columns:
    if c == "titulo_proyecto":
        col_defs.append({
            "field": c,
            "headerName": "Titulo Proyecto",
            "width": 400,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "fecha de publicacion":
        col_defs.append({
            "field": c,
            "headerName": "Fecha de publicacion",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,  # permet le retour à la ligne du header
            "autoHeaderHeight": True
        })
    elif c == "fecha_inicio_contrato":
        col_defs.append({
        "field": c,
        "headerName": "Fecha inicio contrato",
        "width": 100,
        "minWidth": 100,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True
        })
    elif c == "entidad_financiadora":
        col_defs.append({
        "field": c,
        "headerName": "Entidad financiadora",
        # "width": 100,
        "minWidth": 100,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    elif c == "num_plazas":
        col_defs.append({
        "field": c,
        "headerName": "Plazas",
        "width": 60,
        "minWidth": 50,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    elif c == "puesto":
        col_defs.append({
        "field": c,
        "headerName": "Puesto",
        "width": 200,
        "minWidth": 50,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    else:
        col_defs.append({"field": c, "resizable": True})
grid_options = {
    "columnDefs": col_defs,
    "defaultColDef": {"resizable": True, "sortable": True},
    "rowHeight": 50,
    "domLayout": "normal"
}
AgGrid(
    df,
    gridOptions=grid_options,
    # enable_enterprise_modules=False,
    # fit_columns_on_grid_load=False
)
#=============UCM=========================================================================

st.markdown("# Ofertas de la Universidad Complutense de Madrid (UCM)")
st.markdown("Convocatorias con cargo a proyectos:"
            "[https://www.ucm.es/pinves]"
            "(https://www.ucm.es/pinves)")
df = OfferM.merged_offers["ucm"]
col_defs = []
for c in df.columns:
    if c == "titulo_proyecto":
        col_defs.append({
            "field": c,
            "headerName": "Titulo Proyecto",
            "width": 400,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "fecha de publicacion":
        col_defs.append({
            "field": c,
            "headerName": "Fecha de publicacion",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,  # permet le retour à la ligne du header
            "autoHeaderHeight": True
        })
    elif c == "fecha_inicio_contrato":
        col_defs.append({
        "field": c,
        "headerName": "Fecha inicio contrato",
        "width": 100,
        "minWidth": 100,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True
        })
    elif c == "linea_investigacion":
        col_defs.append({
        "field": c,
        "headerName": "Linea de investigacion",
        "width": 500,
        "minWidth": 100,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    elif c == "num_plazas":
        col_defs.append({
        "field": c,
        "headerName": "Plazas",
        "width": 60,
        "minWidth": 50,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    elif c == "puesto":
        col_defs.append({
        "field": c,
        "headerName": "Puesto",
        "width": 200,
        "minWidth": 50,
        "resizable": True,
        "wrapHeaderText": True,  # permet le retour à la ligne du header
        "autoHeaderHeight": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
        })
    else:
        col_defs.append({"field": c, "resizable": True})
grid_options = {
    "columnDefs": col_defs,
    "defaultColDef": {"resizable": True, "sortable": True},
    "domLayout": "normal"
}
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=False
)
#=============UAM=========================================================================

st.markdown("# Ofertas de la Universidad Autonoma de Madrid (UAM)")
st.markdown("Enlace:"
            "[https://aplicaciones.uc3m.es/atenea/publico/1/listarConvocatorias]"
            "(https://aplicaciones.uc3m.es/atenea/publico/1/listarConvocatorias)")
df = pd.read_csv("uam/ofertas_uam.csv")
col_defs = []
for c in df.columns:
    if c == "title":
        col_defs.append({
            "field": c,
            "headerName": "Titulo oferta",
            "width": 1100,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "date":
        col_defs.append({
            "field": c,
            "headerName": "Plazo de solicitud",
            "width": 200,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    else:
        col_defs.append({"field": c, "resizable": True})
grid_options = {
    "columnDefs": col_defs,
    "defaultColDef": {"resizable": True, "sortable": True},
    "domLayout": "normal"
}
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=False
)

#=============UCM=========================================================================

st.markdown("# Ofertas de la Carlos III de Madrid (UC3M)")
st.markdown("Enlace plataforma ATENEA:"
            "[https://web.upm.es/hrs4r/]"
            "(https://web.upm.es/hrs4r/)")
df = pd.read_csv("uc3m/ofertas_uc3m.csv")
col_defs = []
for c in df.columns:
    if c == "codigo":
        col_defs.append({
            "field": c,
            "headerName": "Codigo de oferta",
            "width": 100,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "title":
        col_defs.append({
            "field": c,
            "headerName": "Titulo oferta",
            "width": 600,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "fecha_sol_inicio":
        col_defs.append({
            "field": c,
            "headerName": "Solicitud inicio",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    elif c == "fecha_sol_fin":
        col_defs.append({
            "field": c,
            "headerName": "Solicitud fin",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    elif c == "IP":
        col_defs.append({
            "field": c,
            "headerName": "Responsable",
            "width": 200,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    else:
        col_defs.append({"field": c, "resizable": True})
grid_options = {
    "columnDefs": col_defs,
    "defaultColDef": {"resizable": True, "sortable": True},
    "domLayout": "normal"
}
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=False
)
#=============UCM=========================================================================
st.markdown("# Ofertas de la Universidad Politecnica de Madrid")
st.markdown("Enlace HRS4R UPM:"
            "[https://web.upm.es/hrs4r/]"
            "(https://web.upm.es/hrs4r/)")
col_defs = []
df = pd.read_csv("upm/ofertas_upm.csv")
for c in df.columns:
    print(col_defs)
    if c == "codigo":
        col_defs.append({
            "field": c,
            "headerName": "Codigo de oferta",
            "width": 100,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "title":
        col_defs.append({
            "field": c,
            "headerName": "Titulo oferta",
            "width": 600,
            "minWidth": 200,
            "resizable": True,
            "wrapText": True,
            "autoHeight": True
        })
    elif c == "fecha_sol_inicio":
        col_defs.append({
            "field": c,
            "headerName": "Solicitud inicio",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    elif c == "fecha_sol_fin":
        col_defs.append({
            "field": c,
            "headerName": "Solicitud fin",
            "width": 100,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    elif c == "IP":
        col_defs.append({
            "field": c,
            "headerName": "Responsable",
            "width": 200,
            "minWidth": 100,
            "resizable": True,
            "wrapHeaderText": True,
            "autoHeaderHeight": True
        })
    else:
        col_defs.append({"field": c, "resizable": True})
grid_options = {
    "columnDefs": col_defs,
    "defaultColDef": {"resizable": True, "sortable": True},
    "domLayout": "normal"
}
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=False
)