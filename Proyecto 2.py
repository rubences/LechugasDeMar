import pandas as pd


conversiones=pd.read_csv("conversiones.csv", sep=";")
navegacion=pd.read_csv("navegacion.csv", sep=";")

nav=pd.DataFrame(navegacion)
conv=pd.DataFrame(conversiones)

#Ejercicio 1
#nav.dropna(subset=["url_landing"], inplace=True)
print("Ejercicio 1")
nav=nav.assign(Convertido=0)
conv=conv.assign(Convertido=1)
numeroVisitas=nav.shape[0]
print("El número de visitas es",numeroVisitas)

numeronoconvertidos=len(nav["Convertido"])
numeroconvertidos=len(conv["Convertido"])
numerototal=numeronoconvertidos+numeroconvertidos
print("no convertidos",numeronoconvertidos)
print("convertidos", numeroconvertidos)
print("El porcentaje de convertidos:",(numeroconvertidos/numerototal *100))
print("El porcentaje de no convertidos:",(numeronoconvertidos/numerototal *100))

#Ejercicio 2
print("Ejercicio 2")
freq = conv["lead_type"].value_counts()
print(freq)

#Ejercicio 3
print("Ejercicio 3")
rec= nav["user_recurrent"].value_counts(normalize=True)
print(rec)

#Ejercicio 4
print("Ejercicio 4")
def SacarCoche(URL):
    URL_parts=URL.split("=")
    URL_PARTS=URL_parts[0].split("/")
    if(URL_PARTS[-2]!="es"):
        car=URL_PARTS[-2]
    else:
        car=""
    return car

def contarCoches(Dataframe):
    Coches=pd.DataFrame(columns=["Coches"])
    for i in range (0,len(Dataframe)):
        coche=SacarCoche(Dataframe.iloc[i]["url_landing"])
        if(coche!=""):
            Coches=Coches.append({'Coches':coche}, ignore_index=True)
    return Coches

nav.dropna(subset=["url_landing"], inplace=True)

Coches=contarCoches(nav)
print("El primer coche es el coche con más búsquedas:")
freqcoche=Coches.value_counts()
print(freqcoche)
print(freqcoche[: 1])