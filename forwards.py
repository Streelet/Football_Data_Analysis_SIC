from player import Jugador
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as n


class Delantero(Jugador):
    def __init__(self, nombre, nacionalidad, equipo, edad, valor, dribbles, crosses, goals, assists, shots_on_target):
        super().__init__(nombre, nacionalidad, equipo, edad, valor)
        self.dribbles = dribbles
        self.crosses = crosses
        self.goals = goals
        self.assists = assists
        self.shots_on_target = shots_on_target
    
    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base}, Regates: {self.dribbles}, Centros: {self.crosses}, Goles: {self.goals}, "
                f"Asistencias: {self.assists}, Tiros a Puerta: {self.shots_on_target}")

def cargar_delanteros(archivo_csv):
    # Cargar los datos desde el archivo CSV
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    datos['nationality'] = datos['nationality'].apply(lambda x: ''.join([c for c in x if c.isupper()]))

    # Filtrar los delanteros
    columnas = ['player', 'nationality', 'squad', 'age', 'value', 'dribbles', 'crosses', 'goals', 'assists', 'shots_on_target']
    # Cambié la condición para asegurarnos de que estamos capturando correctamente a los delanteros (RW, LW)
    filtered = datos[datos['position'].str.startswith('FW') ]
    filtered_data = filtered.sort_values('value', ascending=False)

    # Convertir las columnas necesarias a numéricas
    filtered_data['value'] = pd.to_numeric(filtered_data['value'], errors='coerce')
    filtered_data['dribbles_completed'] = pd.to_numeric(filtered_data['dribbles_completed'], errors='coerce')
    filtered_data['crosses'] = pd.to_numeric(filtered_data['crosses'], errors='coerce')
    filtered_data['goals'] = pd.to_numeric(filtered_data['goals'], errors='coerce')
    filtered_data['assists'] = pd.to_numeric(filtered_data['assists'], errors='coerce')
    filtered_data['shots_on_target'] = pd.to_numeric(filtered_data['shots_on_target'], errors='coerce')

    # Crear objetos de tipo Delantero
    delanteros = []
    for _, row in filtered_data.iterrows():
        delantero = Delantero(
            nombre=row['player'],
            nacionalidad=row['nationality'],
            equipo=row['squad'],
            edad=row['age'],
            valor=row['value'],
            dribbles=row['dribbles_completed'],  
            crosses=row['crosses'],
            goals=row['goals'],
            assists=row['assists'],
            shots_on_target=row['shots_on_target'],
        )
        delanteros.append(delantero)

    return delanteros


def graficas_delanteros(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    columnas = [
        'player', 'position', 'nationality', 'squad', 'age',
        'value', 'dribbles', 'crosses', 'goals', 'assists',
        'shots_on_target'
    ]
    filtered_data2 = datos[datos['position'].str.startswith('FW')][columnas]
    filtered_data = filtered_data2.sort_values('value', ascending=False)

    df = filtered_data[['value', 'dribbles', 'crosses', 'goals', 'assists', 'shots_on_target']]
    correlacion = df.corr()

    correlacion1 = correlacion.loc['value', 'dribbles']
    correlacion2 = correlacion.loc['value', 'crosses']
    correlacion3 = correlacion.loc['value', 'goals']
    correlacion4 = correlacion.loc['value', 'assists']
    correlacion5 = correlacion.loc['value', 'shots_on_target']

    suma = correlacion1 + correlacion2 + correlacion3 + correlacion4 + correlacion5
    valores = [
        correlacion1/suma,
        correlacion2/suma,
        correlacion3/suma,
        correlacion4/suma,
        correlacion5/suma,
    ]

    maxc1 = filtered_data['dribbles'].max()
    maxc2 = filtered_data['crosses'].max()
    maxc3 = filtered_data['goals'].max()
    maxc4 = filtered_data['assists'].max()
    maxc5 = filtered_data['shots_on_target'].max()
    maximos = [maxc1, maxc2, maxc3, maxc4, maxc5]
    caracteristicas = ['dribbles', 'crosses', 'goals', 'assists', 'shots_on_target']

    for col, val, max in zip(caracteristicas, valores, maximos):
        filtered_data[col + "_ponderado"] = ((filtered_data[col] - 0)/(max - 0)) * val

    filtered_data['valor_ponderado'] = filtered_data[[col + "_ponderado" for col in caracteristicas]].sum(axis = 1)
    fig1 = px.scatter(filtered_data, x = 'valor_ponderado', y = "value", color = "player", size = "value", title = "Relación Jugadores vs Valor de Mercado")
    figs = []
    figs.append(fig1.to_json())

    fig2 = px.bar(filtered_data.head(10), x='player',
             y=['goals', 'assists', 'shots_on_target'],
             title="Desempeño Comparativo de Delanteros (Top 10)", barmode='group')
    figs.append(fig2.to_json())

    conteo = filtered_data['squad'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo)
    imagen_nube = n.array(nube_palabras.to_image())
    fig3 = px.imshow(imagen_nube, title="Equipos de los Delanteros")
    fig3.update_xaxes(visible=False)
    fig3.update_yaxes(visible=False)
    figs.append(fig3.to_json())

    bins = [0, 20, 25, 30, 35, 40, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40+']
    filtered_data['age_range'] = pd.cut(filtered_data['age'], bins=bins, labels=labels, right=False)
    fig4 = px.pie(filtered_data, names = 'age_range', title = 'Distribución de las Edades')
    figs.append(fig4.to_json())

    fig5 = px.bar(filtered_data.head(16), x='player',
             y=['dribbles'],
             title="Dribbles de Delanteros (Top 15)", barmode='group')
    figs.append(fig5.to_json())
    
    return figs
