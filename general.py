import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import numpy as n

def grafica_general(archivo_csv):
    figs = []
    datos = pd.read_csv(archivo_csv, sep=';', index_col=0)
    datos = datos[datos['age'] > 0]

    # Crear la gráfica
    edades_sumadas = datos['age'].value_counts().sort_index()
    fig1 = px.bar(
        x=edades_sumadas.index,
        y=edades_sumadas.values,
        labels={'x': 'Edad', 'y': 'Número de Jugadores'},
        title="Número de Jugadores por Edad"
    )
    figs.append(fig1.to_json())

    conteo = datos['squad'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo)
    imagen_nube = n.array(nube_palabras.to_image())
    fig2 = px.imshow(imagen_nube, title="Equipos de los Jugadores")
    fig2.update_xaxes(visible=False)
    fig2.update_yaxes(visible=False)
    figs.append(fig2.to_json())

    datos['value'] = pd.to_numeric(datos['value'], errors='coerce')
    fig3 = px.histogram(
            datos, 
            x='value', 
            nbins=50,  # Número de "bins" o intervalos
            title="Distribución del Valor de los Jugadores",
            labels={'Value': 'Valor (USD)'}
        )
    figs.append(fig3.to_json())

    datos['nationality'] = datos['nationality'].apply(lambda x: ''.join([c for c in x if c.isupper()]))
    conteo2 = datos['nationality'].value_counts().to_dict()
    nube_palabras = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    nube_palabras.generate_from_frequencies(conteo2)
    imagen_nube = n.array(nube_palabras.to_image())
    fig4 = px.imshow(imagen_nube, title="Nacionalidad de los Jugadores")
    fig4.update_xaxes(visible=False)
    fig4.update_yaxes(visible=False)
    figs.append(fig4.to_json())

    # Retornar la lista con las gráficas
    return figs
