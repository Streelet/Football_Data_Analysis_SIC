from player import Jugador
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from PIL import Image
import numpy as n


class Defensa(Jugador):
    def __init__(self, nombre, nacionalidad, equipo, edad, valor, entradas_ganadas, intercepciones, despejes, tiros_bloqueados, duelos_ganados):
        super().__init__(nombre, nacionalidad, equipo, edad, valor)
        self.entradas_ganadas = entradas_ganadas
        self.intercepciones = intercepciones
        self.despejes = despejes
        self.tiros_bloqueados = tiros_bloqueados
        self.duelos_ganados = duelos_ganados

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return (f"{info_base}, Entradas Ganadas: {self.entradas_ganadas}, "
                f"Intercepciones: {self.intercepciones}, Despejes: {self.despejes}"
                f"Tiros Bloqueados: {self.tiros_bloqueados}, Duelos Aéreos Ganados: {self.duelos_ganados}")

#Loader para cargar y procesar defensas
def cargar_defensas(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    datos['nationality'] = datos['nationality'].apply(lambda x: ''.join([c for c in x if c.isupper()]))

    # Filtrar los defensas
    columnas = ['player', 'nationality', 'squad', 'age', 'value', 'tackles_won', 'interceptions', 'clearances', 'blocked_shots', 'aerials_won']
    filtered = datos[datos['position'].str.contains('DF', na=False, case=False)][columnas]
    filtered_data = filtered.sort_values('value', ascending=False)

    # Convertir las columnas necesarias a numéricas
    filtered_data['value'] = pd.to_numeric(filtered_data['value'], errors='coerce')
    filtered_data['tackles_won'] = pd.to_numeric(filtered_data['tackles_won'], errors='coerce')
    filtered_data['interceptions'] = pd.to_numeric(filtered_data['interceptions'], errors='coerce')
    filtered_data['clearances'] = pd.to_numeric(filtered_data['clearances'], errors='coerce')
    filtered_data['blocked_shots'] = pd.to_numeric(filtered_data['blocked_shots'], errors='coerce')
    filtered_data['aerials_won'] = pd.to_numeric(filtered_data['aerials_won'], errors='coerce')

    # Crear objetos de tipo Defensas
    defensas = []
    for _, row in filtered_data.iterrows():
        defensa = Defensa(
            nombre=row['player'],
            nacionalidad=row['nationality'],
            equipo=row['squad'],
            edad=row['age'],
            valor=row['value'],
            entradas_ganadas=row['tackles_won'],
            intercepciones=row['interceptions'],
            despejes=row['clearances'],
            tiros_bloqueados=row['blocked_shots'],
            duelos_ganados=row['aerials_won']
        )
        defensas.append(defensa)

    return defensas

def graficas_defensas(archivo_csv):
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]
    columnas = [
    'player', 'position', 'nationality', 'squad', 'age',
    'value', 'height', 'tackles_won', 'interceptions',
    'clearances', 'blocked_shots', 'aerials_won'
    ]

    filtered_data2 = datos[datos['position'].str.startswith('DF')][columnas]
    filtered_data = filtered_data2.sort_values('value', ascending=False)

    df = datos[['value', 'tackles_won', 'interceptions', 'clearances', 'blocked_shots', 'aerials_won', 'age']]
    correlacion = df.corr()

    correlacion1 = correlacion.loc['value', 'tackles_won']
    correlacion2 = correlacion.loc['value', 'interceptions']
    correlacion3 = correlacion.loc['value', 'clearances']
    correlacion4 = correlacion.loc['value', 'blocked_shots']
    correlacion5 = correlacion.loc['value', 'aerials_won']

    suma = correlacion1 + correlacion2 + correlacion3 + correlacion4 + correlacion5
    valor1 = correlacion1/suma
    valor2 = correlacion2/suma
    valor3 = correlacion3/suma
    valor4 = correlacion4/suma
    valor5 = correlacion5/suma
    valores = [valor1, valor2, valor3, valor4, valor5]

    maxc1 = filtered_data['tackles_won'].max()
    maxc2 = filtered_data['interceptions'].max()
    maxc3 = filtered_data['clearances'].max()
    maxc4 = filtered_data['blocked_shots'].max()
    maxc5 = filtered_data['aerials_won'].max()
    maximos = [maxc1, maxc2, maxc3, maxc4, maxc5]

    caracteristicas = ['tackles_won', 'interceptions', 'clearances', 'blocked_shots', 'aerials_won']

    for col, val, max in zip(caracteristicas, valores, maximos):
        filtered_data[col + "_ponderado"] = ((filtered_data[col] - 0)/(max - 0)) * val

    filtered_data['valor_ponderado'] = filtered_data[[col + "_ponderado" for col in caracteristicas]].sum(axis = 1)
    fig1 = px.scatter(filtered_data, x = 'valor_ponderado', y = "value", color = "player", size = "value", title = "Relación Jugadores vs Valor de Mercado")
    figs = []
    figs.append(fig1.to_json())

    fig2 = px.bar(filtered_data.head(10), x='player', 
             y=['tackles_won', 'interceptions', 'blocked_shots', 'aerials_won'],
             title="Desempeño Comparativo de Defensas(Top 10)", barmode='group')
    figs.append(fig2.to_json())

    conteo = filtered_data['squad'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo)
    imagen_nube = n.array(nube_palabras.to_image())
    fig3 = px.imshow(imagen_nube, title="Equipos de los Defensas")
    fig3.update_xaxes(visible=False)
    fig3.update_yaxes(visible=False)
    figs.append(fig3.to_json())

    bins = [0, 20, 25, 30, 35, 40, 100]
    labels = ['<20', '20-24', '25-29', '30-34', '35-39', '40+']
    filtered_data['age_range'] = pd.cut(filtered_data['age'], bins=bins, labels=labels, right=False)
    fig4 = px.pie(filtered_data, names = 'age_range', title = 'Distribución de las Edades')
    figs.append(fig4.to_json())

    fig5 = px.bar(filtered_data.head(18), x='player', 
             y=['clearances'],
             title="Pases Completados de Defensas (Top 15)", barmode='group')
    figs.append(fig5.to_json())
    return figs
