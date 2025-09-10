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
    def __init__(self, uni_list):
        self.date = {}
        self.creader = {}
        self.merged_offers = {}
        for uni in uni_list:
            pdfs_u = glob.glob(uni + "/*.pdf")
            list_date = []
            list_offer = []
            for pdf in pdfs_u:
                reader = ConvocatoriaReader(pdf)
                offers, date = reader.get_offers()
                list_offer.append(offers)
                list_date.append(reader.date)

            if reader.date is not None:
                list_offer = [c for _, c in sorted(zip(list_date, list_offer))]
                list_offer.reverse()
            self.date[uni] = list_date
            self.merged_offers[uni] = pd.concat(list_offer)
            print(f"Processed {reader.pdf_path}")


if __name__ == '__main__':
    offerm = OfferMerger(["ucm", "urjc"])
