
import pandas as pd


#para identificar si hay elementos repetidos
def identificarRepetidos (DataFrame):

    for i in range (0,len(DataFrame)):
        DataFrame2=DataFrame
        if(DataFrame.iloc[i]["id_user"]!= ''):
            DataFrame2= DataFrame.duplicated(DataFrame.columns[~DataFrame.columns.isin(['id_user'])])
        elif(DataFrame.iloc[i]["gclid"]!= ''):
            DataFrame2= DataFrame.duplicated(DataFrame.columns[~DataFrame.columns.isin(['gclid'])])
        else:
            DataFrame2= DataFrame.duplicated(DataFrame.columns[~DataFrame.columns.isin(['url_landing'])])


    return DataFrame2

def eliminarRepetidos (DataFrame):

    for i in range (0, len(DataFrame)):
        DataFrame2=DataFrame
        if(DataFrame.iloc[i]["id_user"]!= ''):
            DataFrame2 = DataFrame.drop_duplicates(DataFrame.columns[~DataFrame.columns.isin(['id_user'])])
        elif(DataFrame.iloc[i]["gclid"]!= ''):
            DataFrame2 = DataFrame.drop_duplicates(DataFrame.columns[~DataFrame.columns.isin(['gclid'])])
        else:
            DataFrame2 = DataFrame.drop_duplicates(DataFrame.columns[~DataFrame.columns.isin(['url_landing'])])


    return DataFrame2

if __name__ == "__main__":
    conversiones=pd.read_csv("conversiones.csv", sep=";")
    navegacion=pd.read_csv("navegacion.csv", sep=";")

    nav=pd.DataFrame(navegacion)
    conv=pd.DataFrame(conversiones)
    print(len(nav))
    print("numero1: " + str(len(nav)))
    nav = eliminarRepetidos(nav)
    print("numero2: " + str(len(nav)))
    nav.sort_values(by=["ts"], inplace=True)
    nav.to_csv("navegacionsort.csv", index=False, sep=";")