import pandas as pd


df = pd.read_csv("export.csv", delimiter=";")
names_per_group = df.groupby("Titel")["Benutzername"].apply(lambda x: ",".join(x))

excel_export = df[["Titel", "Benutzer"]]
excel_export.to_excel("Teilnehmerliste.xlsx")