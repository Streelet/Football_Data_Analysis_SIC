from player import Jugador
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as n

class Mediocampista(Jugador):
    def __init__(self, nombre, nacionalidad, equipo, edad, valor, pases_completados, regates_completados, pases_progresivos, tiros_asistidos):
        super().__init__(nombre, nacionalidad, equipo, edad, valor)
        self.pases_completados = pases_completados
        self.regates_completados = regates_completados
        self.pases_progresivos = pases_progresivos
        self.tiros_asistidos = tiros_asistidos

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base}, Pases Completados: {self.pases_completado}, Regates Completados: {self.regates_completados}, "
                f"Pases Progresivos: {self.pases_progresivos}, Tiros Asistidos: {self.tiros_asistidos}")

def cargar_mediocampistas(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    datos['nationality'] = datos['nationality'].apply(lambda x: ''.join([c for c in x if c.isupper()]))

    # Filtrar los mediocampistas
    columnas = ['player', 'nationality', 'squad', 'age', 'value', 'passes_completed', 'dribbles_completed', 'progressive_passes', 'assisted_shots']
    filtered = datos[datos['position'].str.startswith('MF')][columnas]
    filtered_data = filtered.sort_values('value', ascending=False)

    # Convertir las columnas necesarias a numéricas
    filtered_data['value'] = pd.to_numeric(filtered_data['value'], errors='coerce')
    filtered_data['passes_completed'] = pd.to_numeric(filtered_data['passes_completed'], errors='coerce')
    filtered_data['dribbles_completed'] = pd.to_numeric(filtered_data['dribbles_completed'], errors='coerce')
    filtered_data['progressive_passes'] = pd.to_numeric(filtered_data['progressive_passes'], errors='coerce')
    filtered_data['assisted_shots'] = pd.to_numeric(filtered_data['assisted_shots'], errors='coerce')

    # Crear objetos de tipo Mediocampista
    mediocampistas = []
    for _, row in filtered_data.iterrows():
        mediocampista = Mediocampista(
            nombre=row['player'],
            nacionalidad=row['nationality'],
            equipo=row['squad'],
            edad=row['age'],
            valor=row['value'],
            pases_completados=row['passes_completed'],
            regates_completados=row['dribbles_completed'],
            pases_progresivos=row['progressive_passes'],
            tiros_asistidos=row['assisted_shots']
        )
        mediocampistas.append(mediocampista)

    return mediocampistas

def graficas_mediocampistas(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    columnas = [
    'player', 'position', 'nationality', 'squad', 'age',
    'value', 'height', 'passes_completed', 'dribbles_completed',
    'progressive_passes', 'assisted_shots']
    filtered_data2 = datos[datos['position'].str.startswith('MF')][columnas]
    filtered_data = filtered_data2.sort_values('value', ascending=False)

    df = filtered_data[['value', 'passes_completed', 'dribbles_completed', 'progressive_passes', 'assisted_shots']]
    correlacion = df.corr()

    correlacion1 = correlacion.loc['value', 'passes_completed']
    correlacion2 = correlacion.loc['value', 'dribbles_completed']
    correlacion3 = correlacion.loc['value', 'progressive_passes']
    correlacion4 = correlacion.loc['value', 'assisted_shots']

    suma = correlacion1 + correlacion2 + correlacion3 + correlacion4
    valor1 = correlacion1/suma
    valor2 = correlacion2/suma
    valor3 = correlacion3/suma
    valor4 = correlacion4/suma
    valores = [valor1, valor2, valor3, valor4]

    maxc1 = filtered_data['passes_completed'].max()
    maxc2 = filtered_data['dribbles_completed'].max()
    maxc3 = filtered_data['progressive_passes'].max()
    maxc4 = filtered_data['assisted_shots'].max()
    maximos = [maxc1, maxc2, maxc3, maxc4]
    caracteristicas = ['passes_completed', 'dribbles_completed', 'progressive_passes', 'assisted_shots']

    for col, val, max in zip(caracteristicas, valores, maximos):
        filtered_data[col + "_ponderado"] = ((filtered_data[col] - 0)/(max - 0)) * val

    filtered_data['valor_ponderado'] = filtered_data[[col + "_ponderado" for col in caracteristicas]].sum(axis = 1)
    fig1 = px.scatter(filtered_data, x = 'valor_ponderado', y = "value", color = "player", size = "value", title = "Relación Jugadores vs Valor de Mercado")
    figs = []
    figs.append(fig1.to_json())

    fig2 = px.bar(filtered_data.head(10), x='player', 
             y=['dribbles_completed', 'progressive_passes', 'assisted_shots'],
             title="Desempeño Comparativo de Mediocampistas (Top 10)", barmode='group')
    figs.append(fig2.to_json())

    conteo = filtered_data['squad'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo)
    imagen_nube = n.array(nube_palabras.to_image())
    fig3 = px.imshow(imagen_nube, title="Equipos de los Mediocampistas")
    fig3.update_xaxes(visible=False)
    fig3.update_yaxes(visible=False)
    figs.append(fig3.to_json())

    bins = [0, 20, 25, 30, 35, 40, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40+']
    filtered_data['age_range'] = pd.cut(filtered_data['age'], bins=bins, labels=labels, right=False)
    fig4 = px.pie(filtered_data, names = 'age_range', title = 'Distribución de las Edades')
    figs.append(fig4.to_json())

    fig5 = px.bar(filtered_data.head(15), x='player', 
             y=['passes_completed'],
             title="Pases Completados de Mediocampistas (Top 15)", barmode='group')
    figs.append(fig5.to_json())
    return figs
