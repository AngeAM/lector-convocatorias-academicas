import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from OfferMerger import OfferMerger
from Downloader import urjc_downloader
import pandas as pd

urjc_downloader()
OfferM = OfferMerger()
OfferM.get_offers()
# st.set_page_config(layout="wide")
# st.dataframe(OfferM.df_offers.reset_index(drop=True), height=500)
# st.markdown(
#     OfferM.df_offers.to_html(index=False),
#     unsafe_allow_html=True
# )
#
# # Ajouter du CSS pour augmenter la taille de police
# st.markdown(
#     f"""
#     <style>
#     table {{
#         font-size: 16px;          /* taille police globale */
#         border-collapse: collapse;
#         width: auto;              /* largeur globale auto */
#     }}
#     th, td {{
#         padding: 8px;             /* espace interne */
#         text-align: left;
#         white-space: nowrap;      /* empêcher le retour à la ligne */
#         width: auto;              /* largeur auto selon le contenu */
#     }}
#     </style>
#     {html_table}
#     """,
#     unsafe_allow_html=True
# )
df = OfferM.df_offers
# df = pd.DataFrame({
#     "Universidad": ["URJC", "UAM", "UC3M"],
#     "titulo_proyecto": [
#         "Convenio entre la Comunidad de Madrid y la Universidad Rey Juan Carlos, para la concesión de una subvención directa",
#         "Investigación sobre materiales avanzados para energía de fusión y reactores de IV generación",
#         "Desarrollo de microplataformas fluidicas de bajo coste para caracterización de metales"
#     ],
#     "fecha de publicacion": ["2024-10-01", "2024-11-05", "2024-12-12"]
# })

st.set_page_config(layout="wide")


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



# Vérifie que la largeur est bien dans columnDefs
# st.subheader("columnDefs (debug)")
# st.json(grid_options.get("columnDefs"))

AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=False  # IMPORTANT: empêche AGGrid de réajuster tout à l'ouverture
)