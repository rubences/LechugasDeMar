
import pandas as pd
from paso3proyecto1 import eliminarRepetidos



def juntarTablas(Dataframe1,Dataframe2):

    Dataframe1= eliminarRepetidos(Dataframe1)
    Dataframe2= eliminarRepetidos(Dataframe2)
    Dataframe3= pd.DataFrame()
    if "id_suite" in Dataframe1.columns and "id_suite" in Dataframe2.columns:
        Dataframe3= pd.merge(Dataframe1, Dataframe2, on='id_suite', how='outer',suffixes=("_nav","_conv"))
    elif "gclid" in Dataframe1.columns and "gclid" in Dataframe2.columns:
        Dataframe3= pd.merge(Dataframe1, Dataframe2, on='gclid', how='outer',suffixes=("_nav","_conv"))
    else:
        Dataframe3= pd.merge(Dataframe1, Dataframe2, on='url_landing', how='outer',suffixes=("_nav","_conv"))

    return Dataframe3

if __name__ == "__main__":
    conversiones=pd.read_csv("conversiones.csv", sep=";")
    navegacion=pd.read_csv("navegacion.csv", sep=";")

    nav=pd.DataFrame(navegacion)
    conv=pd.DataFrame(conversiones)
    nav=nav.assign(Convertido=0)
    conv=conv.assign(Convertido=1)

    union= juntarTablas(nav, conv)
    union.to_csv("union.csv", index=False,sep=";")
