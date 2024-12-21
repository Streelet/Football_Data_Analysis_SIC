from player import Jugador
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as n

class Portero(Jugador):
    def __init__(self, nombre, nacionalidad, equipo, edad, valor, goals_against_gk, saves, clean_sheets_pct, passes_completed_gk, crosses_stopped_gk):
        super().__init__(nombre, nacionalidad, equipo, edad, valor)
        self.goals_against_gk = goals_against_gk
        self.saves = saves
        self.clean_sheets_pct = clean_sheets_pct
        self.passes_completed_gk = passes_completed_gk
        self.crosses_stopped_gk = crosses_stopped_gk

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base}, Goles En Contra: {self.goals_against_gk}, Salvadas: {self.saves}, "
                f"Porcentaje de Porterías a Cero: {self.clean_sheets_pct}, Pases Completados: {self.passes_completed_gk}, "
                f"Centros Detenidos: {self.crosses_stopped_gk}")

def cargar_porteros(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    datos['nationality'] = datos['nationality'].apply(lambda x: ''.join([c for c in x if c.isupper()]))

    # Filtrar los porteros
    columnas = ['player', 'nationality', 'squad', 'age', 'value', 'goals_against_gk', 'saves', 'clean_sheets_pct', 'passes_completed_launched_gk', 'crosses_stopped_gk']
    filtered = datos[datos['position'] == 'GK'][columnas]
    filtered_data = filtered.sort_values('value', ascending=False)

    # Convertir las columnas necesarias a numéricas
    filtered_data['value'] = pd.to_numeric(filtered_data['value'], errors='coerce')
    filtered_data['goals_against_gk'] = pd.to_numeric(filtered_data['goals_against_gk'], errors='coerce')
    filtered_data['saves'] = pd.to_numeric(filtered_data['saves'], errors='coerce')
    filtered_data['clean_sheets_pct'] = pd.to_numeric(filtered_data['clean_sheets_pct'], errors='coerce')
    filtered_data['passes_completed_launched_gk'] = pd.to_numeric(filtered_data['passes_completed_launched_gk'], errors='coerce')
    filtered_data['crosses_stopped_gk'] = pd.to_numeric(filtered_data['crosses_stopped_gk'], errors='coerce')

    # Crear objetos de tipo Portero
    porteros = []
    for _, row in filtered_data.iterrows():
        portero = Portero(
            nombre=row['player'],
            nacionalidad=row['nationality'],
            equipo=row['squad'],
            edad=row['age'],
            valor=row['value'],
            goals_against_gk=row['goals_against_gk'],
            saves=row['saves'],
            clean_sheets_pct=row['clean_sheets_pct'],
            passes_completed_gk=row['passes_completed_launched_gk'],
            crosses_stopped_gk=row['crosses_stopped_gk']
        )
        porteros.append(portero)

    return porteros

def graficas_porteros(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    columnas = [
        'player', 'position', 'nationality', 'squad', 'age',
        'value', 'goals_against_gk', 'saves', 'clean_sheets_pct',
        'passes_completed_launched_gk', 'crosses_stopped_gk'
    ]
    filtered_data2 = datos[datos['position'] == 'GK'][columnas]
    filtered_data = filtered_data2.sort_values('value', ascending=False)

    df = filtered_data[['value', 'goals_against_gk', 'saves', 'clean_sheets_pct', 'passes_completed_launched_gk', 'crosses_stopped_gk']]
    correlacion = df.corr()

    correlacion1 = correlacion.loc['value', 'goals_against_gk']
    correlacion2 = correlacion.loc['value', 'saves']
    correlacion3 = correlacion.loc['value', 'clean_sheets_pct']
    correlacion4 = correlacion.loc['value', 'passes_completed_launched_gk']
    correlacion5 = correlacion.loc['value', 'crosses_stopped_gk']

    suma = correlacion1 + correlacion2 + correlacion3 + correlacion4 + correlacion5
    valores = [
        correlacion1/suma,
        correlacion2/suma,
        correlacion3/suma,
        correlacion4/suma,
        correlacion5/suma
    ]

    maxc1 = filtered_data['goals_against_gk'].max()
    maxc2 = filtered_data['saves'].max()
    maxc3 = filtered_data['clean_sheets_pct'].max()
    maxc4 = filtered_data['passes_completed_launched_gk'].max()
    maxc5 = filtered_data['crosses_stopped_gk'].max()
    maximos = [maxc1, maxc2, maxc3, maxc4, maxc5]
    caracteristicas = ['goals_against_gk', 'saves', 'clean_sheets_pct', 'passes_completed_launched_gk', 'crosses_stopped_gk']

    for col, val, max in zip(caracteristicas, valores, maximos):
        filtered_data[col + "_ponderado"] = ((filtered_data[col] - 0)/(max - 0)) * val

    filtered_data['valor_ponderado'] = filtered_data[[col + "_ponderado" for col in caracteristicas]].sum(axis = 1)
    fig1 = px.scatter(filtered_data, x = 'valor_ponderado', y = "value", color = "player", size = "value", title = "Relación Jugadores vs Valor de Mercado")
    figs = []
    figs.append(fig1.to_json())

    fig2 = px.bar(filtered_data.head(10), x='player',
             y=['saves', 'clean_sheets_pct', 'crosses_stopped_gk'],
             title="Desempeño Comparativo de Porteros (Top 10)", barmode='group')
    figs.append(fig2.to_json())

    conteo = filtered_data['squad'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo)
    imagen_nube = n.array(nube_palabras.to_image())
    fig3 = px.imshow(imagen_nube, title="Equipos de los Porteros")
    fig3.update_xaxes(visible=False)
    fig3.update_yaxes(visible=False)
    figs.append(fig3.to_json())

    bins = [0, 20, 25, 30, 35, 40, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40+']
    filtered_data['age_range'] = pd.cut(filtered_data['age'], bins=bins, labels=labels, right=False)
    fig4 = px.pie(filtered_data, names = 'age_range', title = 'Distribución de las Edades')
    figs.append(fig4.to_json())

    fig5 = px.bar(filtered_data.head(15), x='player',
             y=['passes_completed_launched_gk'],
             title="Pases Completados de Porteros (Top 15)", barmode='group')
    figs.append(fig5.to_json())
    
    return figs

