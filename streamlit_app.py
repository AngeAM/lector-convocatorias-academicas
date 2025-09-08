import streamlit as st
st.set_page_config(page_title="Convocatorias", layout="wide")
from OfferMerger import OfferMerger
from Downloader import urjc_downloader

urjc_downloader()
OfferM = OfferMerger()
OfferM.get_offers()
st.title("Ofertas Académicas en España")
st.dataframe(OfferM.df_offers)


