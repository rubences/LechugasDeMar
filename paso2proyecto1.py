import pandas as pd
from pandas.core.frame import DataFrame


#para eliminar los elementos que estén mal buscamos aquellos que no tengan sl(Site link) y los eliminamos
def separarUrl(URL,palabraclave):
    url_parts=URL.split("&")
    camp=0
    ar=[]
    for part in url_parts:
        if "=" in part:
            ar=part.split("=")
            if(len(ar)>2):
                return -1
            else:
                key=ar[0]
                value=ar[1]
            #print(key,value)
            if key==palabraclave:
                camp=value
                break
    return camp

def sacarunaURL(Dataframe,i):
    url=""
    url=Dataframe.iloc[i]["url_landing"]
    return url

def separarUrlColumnaDDF(Dataframe,palabraclave):
    Campa=pd.DataFrame(columns=[palabraclave])
    Data2=Dataframe
    borrados=0
    for i in range (0,len(Data2)):
        camp=separarUrl(sacarunaURL(Data2,i),palabraclave)
        if(camp==-1):
            Dataframe=Dataframe.drop(i-borrados)
            borrados+=1
        else:
            #print(type(Campa))
            Campa=Campa.append({palabraclave:camp}, ignore_index=True)
    return Campa

if __name__ == "__main__":
    conversiones=pd.read_csv("conversiones.csv", sep=";")
    navegacion=pd.read_csv("navegacion.csv", sep=";")

    nav=pd.DataFrame(navegacion)
    conv=pd.DataFrame(conversiones)
    #print(len(nav))
    nav.dropna(subset=["url_landing"], inplace=True)
    #print(len(nav))

    #camp,adg, adv, sl
    #Campaña=separarUrlColumnaDDF(nav,"camp")
    adgroup=separarUrlColumnaDDF(nav,"adg")
    #Adv=separarUrlColumnaDDF(nav,"adv")
    #sl=separarUrlColumnaDDF(nav,"sl")
    #Campaña.to_csv("Campaña.csv")
    adgroup.to_csv("Adgroup.csv", index=False)
    #Adv.to_csv("Adv.csv", index=False)
    #sl.to_csv("sl.csv", index=False)
