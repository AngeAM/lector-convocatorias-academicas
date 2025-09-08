import pandas as pd
from ConvocatoriaReader import ConvocatoriaReader
import glob

mapping = {
        "uc3m": "Universidad Carlos III de Madrid",
        "uam": "Universidad Autónoma de Madrid",
        "urjc": "Universidad Rey Juan Carlos",
        "usal": "Universidad de Salamanca",
        "upm": "Universidad Politécnica de Madrid",
        # ... ajouter les autres
    }

class OfferMerger:
    def __init__(self):
        self.list_df_offers = []
        self.df_offers = None
        self.pdfs_urjc = glob.glob("urjc/*.pdf")
        self.list_creader = []
        self.list_date = []
        for pdf in self.pdfs_urjc:
            reader = ConvocatoriaReader(pdf)
            self.list_creader.append(reader)
            self.list_date.append(reader.date)
            print(f"Processed {reader.pdf_path}")
            # Clasificar las convocatorias por fechas
        self.list_creader.sort(key=lambda x: x.date, reverse=True)

    def get_offers(self):
        for reader in self.list_creader:
            print(f"Processing {reader.pdf_path}")
            reader.get_offers()
            self.list_df_offers.append(reader.offers)
        self.df_offers = pd.concat(self.list_df_offers)




if __name__ == '__main__':
    OfferM = OfferMerger()
    OfferM.get_offers()